# app/model_manager.py

import os
import pandas as pd
from ibm_watson_machine_learning import APIClient
from app.utils.config import Config
from app.utils.logger import Logger

class ModelManager:
    def __init__(self):
        self.logger = Logger.get_logger(self.__class__.__name__)
        self.client = self.get_wml_client()
        self.space_id = Config.WML_SPACE_ID
        self.model_uid = None
        self.deployment_uid = None

    def get_wml_client(self):
        wml_credentials = {
            "apikey": Config.WML_API_KEY,
            "url": Config.WML_URL,
        }
        client = APIClient(wml_credentials)
        if self.space_id:
            client.set.default_space(self.space_id)
        else:
            self.logger.error("WML Space ID is not set in the configuration.")
            raise ValueError("WML Space ID is required.")
        return client

    def train_or_load_model(self, force_retrain=False):
        try:
            if force_retrain or not self.check_model_exists():
                self.train_and_deploy_model()
            else:
                self.logger.info("Model exists in IBM Watson Machine Learning. Skipping retraining.")
        except Exception as e:
            self.logger.exception(f"Failed to train or load model: {e}")
            raise

    def check_model_exists(self):
        models = self.client.repository.get_model_details()
        for model in models.get('resources', []):
            if model['entity']['name'] == Config.MODEL_NAME:
                self.model_uid = model['metadata']['id']
                self.logger.info(f"Found existing model with UID: {self.model_uid}")
                return True
        return False

    def train_and_deploy_model(self):
        if not os.path.exists(Config.DATASET_FILE):
            self.logger.error(f"No dataset found at {Config.DATASET_FILE}. Cannot retrain.")
            raise FileNotFoundError(f"{Config.DATASET_FILE} not found.")

        self.logger.info("Reading dataset...")
        data = pd.read_csv(Config.DATASET_FILE)
        self.logger.info("Starting model training...")
        self.train_model(data)

    def train_model(self, data):
        try:
            metadata = {
                self.client.training.ConfigurationMetaNames.NAME: Config.MODEL_NAME,
                self.client.training.ConfigurationMetaNames.TRAINING_DATA_REFERENCES: [{
                    "connection": {
                        "endpoint_url": Config.COS_ENDPOINT,
                        "access_key_id": Config.COS_ACCESS_KEY_ID,
                        "secret_access_key": Config.COS_SECRET_ACCESS_KEY
                    },
                    "source": {
                        "bucket": Config.COS_BUCKET_NAME,
                        "object_key": Config.DATASET_FILE
                    },
                    "type": "s3"
                }],
                self.client.training.ConfigurationMetaNames.TRAINING_RESULTS_REFERENCE: {
                    "connection": {
                        "endpoint_url": Config.COS_ENDPOINT,
                        "access_key_id": Config.COS_ACCESS_KEY_ID,
                        "secret_access_key": Config.COS_SECRET_ACCESS_KEY
                    },
                    "target": {
                        "bucket": Config.COS_BUCKET_NAME
                    },
                    "type": "s3"
                },
                self.client.training.ConfigurationMetaNames.EXPERIMENT_NAME: Config.EXPERIMENT_NAME,
                self.client.training.ConfigurationMetaNames.TAGS: ["autoai", "regression"],
            }

            experiment_info = self.client.training.run(meta_props=metadata)
            training_uid = self.client.training.get_id(experiment_info)
            self.logger.info(f"Training started with UID: {training_uid}")

            self.client.training.wait_for_training(training_uid)
            self.logger.info("Training completed.")

            training_details = self.client.training.get_details(training_uid)
            model_uid = self.client.training.get_model_id(training_details)
            self.model_uid = model_uid
            self.logger.info(f"Trained model UID: {self.model_uid}")

            self.deploy_model()
        except Exception as e:
            self.logger.exception(f"Failed to train model: {e}")
            raise

    def deploy_model(self):
        try:
            deployment_details = self.client.deployments.create(
                artifact_uid=self.model_uid,
                meta_props={
                    self.client.deployments.ConfigurationMetaNames.NAME: Config.DEPLOYMENT_NAME,
                    self.client.deployments.ConfigurationMetaNames.ONLINE: {}
                }
            )
            self.deployment_uid = self.client.deployments.get_uid(deployment_details)
            self.logger.info(f"Model deployed with UID: {self.deployment_uid}")
        except Exception as e:
            self.logger.exception(f"Failed to deploy model: {e}")
            raise

    def maybe_retrain_model(self):
        try:
            data = pd.read_csv(Config.DATASET_FILE)
            if len(data) % Config.RETRAIN_THRESHOLD == 0:
                self.logger.info("Retrain threshold reached. Retraining model...")
                self.train_or_load_model(force_retrain=True)
            else:
                self.logger.info("Retrain threshold not reached. Skipping retraining.")
        except Exception as e:
            self.logger.exception(f"Failed during maybe_retrain_model: {e}")
            raise