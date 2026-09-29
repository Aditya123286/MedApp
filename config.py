import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Base configuration"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key-change-in-production')
    
    # Database
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Email Configuration
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'True').lower() == 'true'
    MAIL_USE_SSL = os.getenv('MAIL_USE_SSL', 'False').lower() == 'true'
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER')
    MAIL_MAX_EMAILS = int(os.getenv('MAIL_MAX_EMAILS', 5))
    
    # Redis/Celery
    REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
    CELERY_BROKER_URL = REDIS_URL
    CELERY_RESULT_BACKEND = REDIS_URL
    
    # Security
    BCRYPT_ROUNDS = int(os.getenv('BCRYPT_ROUNDS', 12))
    PASSWORD_RESET_EXPIRY = int(os.getenv('PASSWORD_RESET_EXPIRY', 3600))

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    FLASK_ENV = 'development'
    MAIL_SUPPRESS_SEND = False  # Actually send emails in dev

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    FLASK_ENV = 'production'
    
    # Production email settings
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    DEBUG = True
    MAIL_SUPPRESS_SEND = True  # Don't actually send emails in tests
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}