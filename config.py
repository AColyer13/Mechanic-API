import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration class"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'mysql+mysqlconnector://root:password@localhost/mechanicshopdata'
    # Disable SSL to avoid Python 3.14 SSL certificate bug on Windows
    SQLALCHEMY_ENGINE_OPTIONS = {'connect_args': {'ssl_disabled': True}}

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'mysql+mysqlconnector://root:password@localhost/mechanicshopdata'
    SQLALCHEMY_ENGINE_OPTIONS = {'connect_args': {'ssl_disabled': True}}

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:password@localhost/mechanicshopdata_test'
    SQLALCHEMY_ENGINE_OPTIONS = {'connect_args': {'ssl_disabled': True}}

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}