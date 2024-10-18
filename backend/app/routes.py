from flask import Blueprint, request, jsonify
from app.ml.model import process_sensor_data, predict_feed_amount, train_or_load_model
import logging

api = Blueprint('api', __name__)

@api.route("/health", methods=["GET"])
def health_check():
    """
    Health check endpoint to ensure the API is running.
    
    Returns:
        JSON response indicating the status of the service.
    """
    return jsonify({"status": "UP"}), 200

@api.route("/predict", methods=["POST"])
def predict():
    """
    Predicts the optimal feed amount based on incoming sensor data.

    Request JSON:
        Sensor data for the model to predict.

    Returns:
        JSON response with the prediction or error message.
    """
    if not request.is_json:
        return jsonify({"error": "Request data must be in JSON format"}), 400

    try:
        sensor_data = request.get_json()
        process_sensor_data(sensor_data)
        prediction = predict_feed_amount(sensor_data)
        return jsonify({"prediction": prediction}), 200
    except Exception as e:
        logging.error(f"Error during prediction: {str(e)}")
        return jsonify({"error": "Failed to process the request"}), 500

@api.route("/retrain", methods=["POST"])
def retrain_model():
    """
    Forces model retraining.

    Returns:
        JSON response indicating success or failure.
    """
    try:
        train_or_load_model(force_retrain=True)
        return jsonify({"status": "Model retrained successfully"}), 200
    except Exception as e:
        logging.error(f"Error during retraining: {str(e)}")
        return jsonify({"error": "Failed to retrain the model"}), 500