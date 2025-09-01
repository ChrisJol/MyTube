from flask import Flask
from flask_cors import CORS
import os
from dotenv import load_dotenv
from .config import config

def create_app(config_name=None):
    """Flask application factory"""
    load_dotenv()

    # Get configuration
    config_name = config_name or os.getenv('FLASK_ENV', 'default')
    app_config = config[config_name]

    # Configure Flask to serve Vue SPA directly from dist folder
    app = Flask(__name__,
                static_folder=app_config.get_frontend_path(),
                static_url_path='')
    CORS(app)

    # Load configuration
    app.config.from_object(app_config)

    # Register blueprints
    from .routes.dashboard import dashboard_bp
    from .api.base import api_base_bp
    from .api.videos import videos_api_bp

    app.register_blueprint(dashboard_bp)
    app.register_blueprint(api_base_bp)
    app.register_blueprint(videos_api_bp)

    return app
