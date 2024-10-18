import os
import pandas as pd
import joblib
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import logging
from app.config import Config

# Global model variable
model = None

def train_or_load_model(force_retrain=False):
    """
    Trains or loads the RandomForestRegressor model from the dataset.
    
    Args:
        force_retrain (bool): If True, retrains the model even if a pre-trained model exists.

    Returns:
        None
    """
    global model
    if not os.path.exists(Config.MODEL_FILENAME) or force_retrain:
        if os.path.exists(Config.DATASET_FILE):
            logging.info("Retraining the model from the dataset...")
            data = pd.read_csv(Config.DATASET_FILE)

            # Define features and target variable
            features = ["fish_size_kg", "fish_length_cm", "water_temperature_C", "phosphorus_mg_L", 
                        "nitrogen_mg_L", "oxygen_mg_L", "light_LUX", "fish_speed_m_s", "fish_health"]
            target = "excess_feed_kg"
            X = data[features]
            y = data[target]

            # Split the data into training and testing sets
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

            # Initialize and train the model
            model = RandomForestRegressor(n_estimators=100, random_state=42)
            model.fit(X_train, y_train)

            # Evaluate the model
            y_pred = model.predict(X_test)
            mse = mean_squared_error(y_test, y_pred)
            logging.info(f"Model retrained. Mean Squared Error: {mse}")

            # Save the updated model
            joblib.dump(model, Config.MODEL_FILENAME)
            logging.info(f"Model saved as {Config.MODEL_FILENAME}")
        else:
            logging.error(f"No dataset found at {Config.DATASET_FILE}. Cannot retrain.")
    else:
        model = joblib.load(Config.MODEL_FILENAME)
        logging.info(f"Model loaded from {Config.MODEL_FILENAME}")

def predict_feed_amount(sensor_data):
    """
    Predicts the optimal feed amount based on sensor data.

    Args:
        sensor_data (DataFrame): Sensor data for prediction.

    Returns:
        float: The predicted feed amount.
    """
    global model
    if model is None:
        logging.info("Model is not loaded. Training or loading model...")
        train_or_load_model()

    prediction = model.predict(sensor_data)
    logging.info(f"Predicted optimal feed amount: {prediction[0]} grams")
    return prediction[0]

def process_sensor_data(sensor_data):
    """
    Processes incoming sensor data and saves it to the dataset file.
    
    Args:
        sensor_data (dict): Incoming sensor data.

    Returns:
        None
    """
    sensor_df = pd.DataFrame([sensor_data])
    
    if os.path.exists(Config.DATASET_FILE):
        sensor_df.to_csv(Config.DATASET_FILE, mode='a', header=False, index=False)
    else:
        sensor_df.to_csv(Config.DATASET_FILE, mode='w', index=False)
    
    maybe_retrain_model()

def maybe_retrain_model():
    """
    Retrains the model when the retrain threshold is reached.
    
    Returns:
        None
    """
    data = pd.read_csv(Config.DATASET_FILE)
    if len(data) % Config.RETRAIN_THRESHOLD == 0:
        train_or_load_model(force_retrain=True)