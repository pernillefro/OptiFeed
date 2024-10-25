from flask import Flask
from app.utils.config import Config
from app.routes import api

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Register Blueprints (for API routes)
    app.register_blueprint(api)

    return app