# tests/test_model.py

import unittest
import pandas as pd
from app.model_manager import ModelManager
from app.predictor import Predictor
from app.utils.config import Config

class TestModel(unittest.TestCase):
    def test_train_and_predict(self):
        # Initialise the ModelManager and force retraining
        model_manager = ModelManager()
        model_manager.train_or_load_model(force_retrain=True)
        
        # Prepare sample sensor data
        sensor_data = pd.DataFrame([{
            "fish_size_kg": 2.3,
            "fish_length_cm": 50,
            "water_temperature_C": 15,
            "phosphorus_mg_L": 2.0,
            "nitrogen_mg_L": 0.5,
            "oxygen_mg_L": 5.0,
            "light_LUX": 3000,
            "fish_speed_m_s": 0.2,
            "fish_health": 1
        }])

        # Ensure the data contains only the features expected by the model
        features = Config.FEATURES
        sensor_data = sensor_data[features]

        # Initialise the Predictor and make a prediction
        predictor = Predictor()
        prediction = predictor.predict_feed_amount(sensor_data)

        # Check that the prediction is a non-negative float
        self.assertIsInstance(prediction, float)
        self.assertGreaterEqual(prediction, 0)

if __name__ == "__main__":
    unittest.main()