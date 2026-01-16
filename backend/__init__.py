"""
Backend package initialization and app factory.
"""
from flask import Flask
from flask_cors import CORS
from backend.models import db
from backend.config import config
from src.logger import logging
import os

def create_app(config_name=None):
    """Application factory pattern"""
    app = Flask(__name__)
    
    # Load configuration
    config_name = config_name or os.getenv('FLASK_ENV', 'development')
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    
    # Configure CORS
    CORS(app, origins=app.config['CORS_ORIGINS'], supports_credentials=True)
    
    # Register blueprints
    from backend.routes.auth import auth_bp
    from backend.routes.analysis import analysis_bp
    from backend.routes.resources import resources_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(analysis_bp)
    app.register_blueprint(resources_bp)
    
    # Health check endpoint
    @app.route('/api/health', methods=['GET'])
    def health():
        return {'status': 'healthy'}, 200
    
    # Create database tables
    with app.app_context():
        db.create_all()
        logging.info("Database tables created/verified")
    
    return app
