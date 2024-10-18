import unittest
from app import create_app

class TestRoutes(unittest.TestCase):
    def setUp(self):
        self.app = create_app().test_client()
        self.app.testing = True

    def test_health_check(self):
        response = self.app.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertIn("UP", response.get_json()["status"])

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
        response = self.app.post("/predict", json=sensor_data)
        self.assertEqual(response.status_code, 200)

    def test_retrain(self):
        response = self.app.post("/retrain")
        self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()