# app/predictor.py

import pandas as pd
from ibm_watson_machine_learning import APIClient
from app.config import Config
from app.logger import Logger

class Predictor:
    def __init__(self):
        self.logger = Logger.get_logger(self.__class__.__name__)
        self.client = self.get_wml_client()
        self.deployment_uid = self.get_deployment_uid()

    def get_wml_client(self):
        wml_credentials = {
            "apikey": Config.WML_API_KEY,
            "url": Config.WML_URL,
        }
        client = APIClient(wml_credentials)
        if Config.WML_SPACE_ID:
            client.set.default_space(Config.WML_SPACE_ID)
        else:
            self.logger.error("WML Space ID is not set in the configuration.")
            raise ValueError("WML Space ID is required.")
        return client

    def get_deployment_uid(self):
        deployments = self.client.deployments.get_details()
        for deployment in deployments.get('resources', []):
            if deployment['entity']['name'] == Config.DEPLOYMENT_NAME:
                deployment_uid = deployment['metadata']['id']
                self.logger.info(f"Found deployment UID: {deployment_uid}")
                return deployment_uid
        self.logger.error(f"No deployment found with name {Config.DEPLOYMENT_NAME}.")
        raise Exception(f"Deployment {Config.DEPLOYMENT_NAME} not found.")

    def predict_feed_amount(self, sensor_data):
        payload = {
            self.client.deployments.ScoringMetaNames.INPUT_DATA: [{
                'fields': sensor_data.columns.tolist(),
                'values': sensor_data.values.tolist()
            }]
        }
        try:
            predictions = self.client.deployments.score(self.deployment_uid, payload)
            prediction = predictions['predictions'][0]['values'][0][0]
            self.logger.info(f"Predicted optimal feed amount: {prediction} kg")
            return prediction
        except Exception as e:
            self.logger.exception(f"Prediction failed: {e}")
            raise