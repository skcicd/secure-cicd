# This file initializes the Flask app and loads the configuration.
from flask import Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from config import Config

def create_app():
    app = Flask(__name__)

    # Load configuration
    app.config.from_object(Config)

    # Initialize rate limiter
    limiter = Limiter(
        get_remote_address,
        app=app,
        default_limits=["200 per day", "50 per hour"], #applies to all routes unless overridden.

    )

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

