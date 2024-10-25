# app/routes.py

from flask import Blueprint, request, jsonify
from app.data_processor import DataProcessor
from app.model_manager import ModelManager
from app.predictor import Predictor
from app.utils.config import Config
import pandas as pd
import logging

api = Blueprint('api', __name__)

@api.route("/health", methods=["GET"])
def health_check():
    """
    Health check endpoint to ensure the API is running.
    """
    return jsonify({"status": "UP"}), 200

@api.route("/predict", methods=["POST"])
def predict():
    """
    Predicts the optimal feed amount based on incoming sensor data.
    """
    if not request.is_json:
        return jsonify({"error": "Request data must be in JSON format"}), 400

    try:
        sensor_data = request.get_json()

        # Initialise DataProcessor and process the sensor data
        data_processor = DataProcessor()
        data_processor.process_sensor_data(sensor_data)

        # Prepare data for prediction (exclude target variable if present)
        features = Config.FEATURES
        sensor_df = pd.DataFrame([sensor_data])
        sensor_df = sensor_df[features]

        # Initialise Predictor and make prediction
        predictor = Predictor()
        prediction = predictor.predict_feed_amount(sensor_df)

        # Check if retraining is needed
        model_manager = ModelManager()
        model_manager.maybe_retrain_model()

        return jsonify({"prediction": prediction}), 200
    except Exception as e:
        logging.exception(f"Error during prediction: {str(e)}")
        return jsonify({"error": "Failed to process the request"}), 500

@api.route("/retrain", methods=["POST"])
def retrain_model():
    """
    Forces model retraining.
    """
    try:
        model_manager = ModelManager()
        model_manager.train_or_load_model(force_retrain=True)
        return jsonify({"status": "Model retrained successfully"}), 200
    except Exception as e:
        logging.exception(f"Error during retraining: {str(e)}")
        return jsonify({"error": "Failed to retrain the model"}), 500