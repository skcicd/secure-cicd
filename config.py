import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
INSTANCE_DIR = os.path.join(BASE_DIR, "instance")

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default-secret-key')  # Use a strong key in production
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(INSTANCE_DIR, 'app.db')}"  # Path to SQLite database
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Disable track modifications for performance
    OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY')
    DEBUG = False
    TESTING = False
