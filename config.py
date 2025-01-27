import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default-secret-key')  # Use a strong key in production
    DEBUG = False
    TESTING = False

print(f"Loaded SECRET_KEY: {Config.SECRET_KEY}")  # Debug output