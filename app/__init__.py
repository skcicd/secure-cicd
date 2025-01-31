# This file initializes the Flask app and loads the configuration.
from flask import Flask, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from config import Config
from flask_sqlalchemy import SQLAlchemy
from redis import Redis
import os

db = SQLAlchemy()

def exempt_local_ip():
    return get_remote_address() == "127.0.0.1"  # Exempt localhost

# Initialize the Limiter
limiter = Limiter(
    get_remote_address,
    default_limits=["200 per day", "50 per hour"],  # Global default limit
    application_limits_exempt_when=exempt_local_ip,  # Exempt localhost
    storage_uri=os.getenv("REDIS_URL", "redis://redis:6379/0"),  # Use Redis as storage
    )

def create_app():
    app = Flask(__name__)

    limiter.init_app(app)

    # Load configuration
    app.config.from_object(Config)

    # Initialize Redis connection
    redis = Redis.from_url(app.config["RATELIMIT_STORAGE_URL"])

    # Initialize SQLAlchemy
    db.init_app(app)
    
    # Register blueprints (routes)
    with app.app_context():
        from . import routes
        app.register_blueprint(routes.bp)

    


    # Set security headers
    @app.after_request
    def set_security_headers(response):
        response.headers['Content-Security-Policy'] = "default-src 'self';"
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        return response
    
    


    return app

