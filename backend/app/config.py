import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    FLASK_ENV = os.getenv("FLASK_ENV", "production")
    SECRET_KEY = os.getenv("SECRET_KEY", "secret-key")
    IBM_API_KEY_ID = os.getenv("IBM_API_KEY_ID")
    IBM_SERVICE_INSTANCE_ID = os.getenv("IBM_SERVICE_INSTANCE_ID")
    IBM_ENDPOINT_URL = os.getenv("IBM_ENDPOINT_URL")
    COS_BUCKET_NAME = os.getenv("COS_BUCKET_NAME")
    RETRAIN_THRESHOLD = int(os.getenv("RETRAIN_THRESHOLD", 50))
    PORT = int(os.getenv("PORT", 5000))
    MODEL_FILENAME = "optifeed_model.pkl"
    DATASET_FILE = "salmon_farm_training_data.csv"