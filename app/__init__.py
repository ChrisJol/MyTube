from flask import Flask
from flask_cors import CORS
import os
from dotenv import load_dotenv

def create_app():
    """Flask application factory"""
    load_dotenv()

    app = Flask(__name__, template_folder='../templates')
    CORS(app)

    # Configuration
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
    app.config['DATABASE_PATH'] = os.getenv('DATABASE_PATH', 'video_inspiration.db')

    # Register blueprints
    from .routes.dashboard import dashboard_bp
    from .api.base import api_base_bp
    from .api.videos import videos_api_bp

    app.register_blueprint(dashboard_bp)
    app.register_blueprint(api_base_bp)
    app.register_blueprint(videos_api_bp)

    return app
