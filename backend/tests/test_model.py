import unittest
import pandas as pd
from app.ml.model import train_or_load_model, predict_feed_amount

class TestModel(unittest.TestCase):
    def test_train_or_load_model(self):
        train_or_load_model(force_retrain=True)
        # Check if the model was trained successfully by running predictions
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
        prediction = predict_feed_amount(sensor_data)
        self.assertGreaterEqual(prediction, 0)

if __name__ == "__main__":
    unittest.main()