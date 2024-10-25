# app/data_processor.py

import os
import pandas as pd
from app.utils.config import Config
from app.utils.logger import Logger

class DataProcessor:
    def __init__(self):
        self.logger = Logger.get_logger(self.__class__.__name__)

    def process_sensor_data(self, sensor_data):
        try:
            sensor_df = pd.DataFrame([sensor_data])
            self.validate_data(sensor_df)
            self.save_data(sensor_df)
        except Exception as e:
            self.logger.exception(f"Failed to process sensor data: {e}")
            raise

    def validate_data(self, sensor_df):
        required_columns = set(Config.FEATURES)
        missing_columns = required_columns - set(sensor_df.columns)
        if missing_columns:
            self.logger.error(f"Missing required data fields: {missing_columns}")
            raise ValueError(f"Missing fields: {missing_columns}")
        self.logger.info("Data validation passed.")

    def save_data(self, sensor_df):
        file_exists = os.path.exists(Config.DATASET_FILE)
        mode = 'a' if file_exists else 'w'
        header = not file_exists
        sensor_df.to_csv(Config.DATASET_FILE, mode=mode, header=header, index=False)
        self.logger.info(f"Sensor data saved to {Config.DATASET_FILE}")