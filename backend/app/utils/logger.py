# app/logger.py

import logging
from logging.handlers import RotatingFileHandler
from app.utils.config import Config

class Logger:
    _logger_initialized = False

    @classmethod
    def setup_logging(cls):
        if cls._logger_initialized:
            return
        log_level = getattr(logging, Config.LOG_LEVEL.upper(), logging.INFO)
        handler = RotatingFileHandler(Config.LOG_FILE, maxBytes=10485760, backupCount=5)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)

        logger = logging.getLogger()
        logger.setLevel(log_level)
        logger.addHandler(handler)
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        cls._logger_initialized = True

    @classmethod
    def get_logger(cls, name):
        if not cls._logger_initialized:
            cls.setup_logging()
        return logging.getLogger(name)