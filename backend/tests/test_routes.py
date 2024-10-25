# tests/test_routes.py

import unittest
from app import create_app

class TestRoutes(unittest.TestCase):
    def setUp(self):
        app = create_app()
        app.testing = True
        self.client = app.test_client()

    def test_health_check(self):
        response = self.client.get("/api/health")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn("status", data)
        self.assertEqual(data["status"], "UP")

    def test_predict(self):
        sensor_data = {
            "fish_size_kg": 2.3,
            "fish_length_cm": 50,
            "water_temperature_C": 15,
            "phosphorus_mg_L": 2.0,
            "nitrogen_mg_L": 0.5,
            "oxygen_mg_L": 5.0,
            "light_LUX": 3000,
            "fish_speed_m_s": 0.2,
            "fish_health": 1
        }
        response = self.client.post("/api/predict", json=sensor_data)
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn("prediction", data)
        self.assertIsInstance(data["prediction"], (int, float))
        self.assertGreaterEqual(data["prediction"], 0)

    def test_retrain(self):
        response = self.client.post("/api/retrain")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn("status", data)
        self.assertEqual(data["status"], "Model retrained successfully")

if __name__ == "__main__":
    unittest.main()