import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration class."""
    
    # Flask Configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    DEBUG = os.getenv('FLASK_ENV', 'development') == 'development'
    
    # Oracle Database Configuration - .env se lenge
    ORACLE_USER = os.getenv('ORACLE_USER', 'system')
    ORACLE_PASSWORD = os.getenv('ORACLE_PASSWORD', '1234')
    ORACLE_HOST = os.getenv('ORACLE_HOST', 'localhost')
    ORACLE_PORT = os.getenv('ORACLE_PORT', '1521')
    ORACLE_SERVICE = os.getenv('ORACLE_SERVICE', 'XE')
    ORACLE_DSN = os.getenv('ORACLE_DSN', 'localhost:1521/XE')
    
    # JWT Configuration
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(seconds=int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES', 86400)))
    
    # CORS Configuration
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:3000,http://localhost:5500').split(',')
    
    # API Configuration
    API_PREFIX = os.getenv('API_PREFIX', '/api/v1')
    
    # Application Info
    APP_NAME = os.getenv('APP_NAME', 'MedApp')
    VERSION = "1.0.0"


class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True


class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    SQLALCHEMY_ECHO = False


class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}