import os
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask
from flask_jwt_extended import JWTManager
from flasgger import Flasgger
from config import config
from app.models import db
from app.routes.auth import auth_bp
from app.routes.tasks import tasks_bp
from app.routes.admin import admin_bp

def setup_logging(app):
    """Configure structured logging for the application"""
    if not os.path.exists('logs'):
        os.mkdir('logs')
    
    # Standard format for log entries
    formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
    )
    
    # 1. Info level logger for general app activity
    info_handler = RotatingFileHandler(
        'logs/app.log', 
        maxBytes=1024 * 1024 * 5,  # 5MB per file
        backupCount=5              # Keep 5 historical logs
    )
    info_handler.setLevel(logging.INFO)
    info_handler.setFormatter(formatter)
    
    # 2. Error level logger for better debugging in production
    error_handler = RotatingFileHandler(
        'logs/error.log', 
        maxBytes=1024 * 1024 * 5, 
        backupCount=10
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(formatter)
    
    # Clear existing handlers to prevent duplicates if app is re-initialized
    app.logger.handlers.clear()
    
    # Add handlers to Flask app logger
    app.logger.addHandler(info_handler)
    app.logger.addHandler(error_handler)
    app.logger.setLevel(logging.INFO)
    
    app.logger.info('--- Logging setup complete. Application starting... ---')

def create_app(config_name=None):
    """Application factory function"""
    
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
    
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Initialize Logging
    setup_logging(app)
    
    # Initialize extensions
    db.init_app(app)
    JWTManager(app)
    
    # Ensure the instance folder exists for SQLite
    db_uri = app.config.get('SQLALCHEMY_DATABASE_URI', '')
    if db_uri and db_uri.startswith('sqlite:///'):
        # Extract the filesystem path from the URI
        # sqlite:///relative/path -> relative/path
        # sqlite:////absolute/path -> /absolute/path
        db_path = db_uri.replace('sqlite:///', '')
        
        # Get the directory part of the path
        db_dir = os.path.dirname(os.path.abspath(db_path))
        
        if db_dir and not os.path.exists(db_dir):
            app.logger.info(f"Creating database directory: {db_dir}")
            os.makedirs(db_dir, exist_ok=True)
    
    # Initialize Flasgger for Swagger documentation
    swagger = Flasgger(app, template={
        "swagger": "2.0",
        "info": {
            "title": "Task Manager API",
            "description": "A comprehensive RESTful API for managing tasks with user authentication and role-based access control. Features include user registration/login, task CRUD operations, and admin user management.",
            "version": "1.0.0",
            "contact": {
                "name": "Task Manager API Support",
                "email": "support@taskmanager.local"
            },
            "license": {
                "name": "MIT"
            }
        },
        "basePath": "/",
        "schemes": ["http"],
        "consumes": ["application/json"],
        "produces": ["application/json"],
        "securityDefinitions": {
            "Bearer": {
                "type": "apiKey",
                "name": "Authorization",
                "in": "header",
                "description": "JWT Bearer token for authentication. Format: 'Bearer <your_jwt_token>'",
            }
        },
        "tags": [
            {
                "name": "Authentication",
                "description": "User registration, login, and profile management"
            },
            {
                "name": "Tasks",
                "description": "CRUD operations for tasks with pagination and filtering"
            },
            {
                "name": "Admin",
                "description": "Administrative endpoints for user and task management (admin only)"
            },
            {
                "name": "Health",
                "description": "Service health check endpoint"
            }
        ]
    })
    
    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(tasks_bp)
    app.register_blueprint(admin_bp)
    
    # Health check endpoint
    @app.route('/api/health', methods=['GET'])
    def health_check():
        """
        Health check endpoint
        Simple endpoint to verify API is running and healthy.
        ---
        tags:
          - Health
        summary: Check API health
        description: Returns API health status. No authentication required.
        responses:
          200:
            description: API is running and healthy
            schema:
              type: object
              properties:
                status:
                  type: string
                  example: "healthy"
                  description: Service status
        """
        return {'status': 'healthy'}, 200
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
