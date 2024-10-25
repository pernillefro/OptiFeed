# app/config.py

import os

class Config:
    # File paths
    DATASET_FILE = 'dataset.csv'

    # Model settings
    RETRAIN_THRESHOLD = 100
    TARGET = "excess_feed_kg"
    FEATURES = [
        "fish_size_kg",
        "fish_length_cm",
        "water_temperature_C",
        "phosphorus_mg_L",
        "nitrogen_mg_L",
        "oxygen_mg_L",
        "light_LUX",
        "fish_speed_m_s",
        "fish_health"
    ]

    # IBM Watson Machine Learning credentials and settings
    WML_API_KEY = os.getenv('WML_API_KEY')
    WML_URL = os.getenv('WML_URL', 'https://us-south.ml.cloud.ibm.com')
    WML_SPACE_ID = os.getenv('WML_SPACE_ID')
    MODEL_NAME = 'Random Forest Regressor Model'
    DEPLOYMENT_NAME = 'Model Deployment'
    EXPERIMENT_NAME = 'AutoAI Experiment'

    # IBM Cloud Object Storage credentials
    COS_ENDPOINT = os.getenv('COS_ENDPOINT')
    COS_ACCESS_KEY_ID = os.getenv('COS_ACCESS_KEY_ID')
    COS_SECRET_ACCESS_KEY = os.getenv('COS_SECRET_ACCESS_KEY')
    COS_BUCKET_NAME = os.getenv('COS_BUCKET_NAME')

    # Logging settings
    LOG_LEVEL = 'INFO'