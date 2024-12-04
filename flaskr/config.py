import os

class Config:
    """Base configuration"""
    SECRET_KEY = 'default_secret'
    CORS_HEADER = 'application/json'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    UPLOAD_FOLDER = None
    PROCESSED_FOLDER = None
    MODEL_PATH = None
    DEBUG = None
    CELERY = None
    DATABASE = None
    
class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    CELERY = {
        'broker_url': 'redis://localhost:6379/0',
        'result_backend': 'redis://localhost:6379/0',
        'task_track_started': True,
        'task_ignore_result': False,
        'result_serializer': 'json',
    }
    UPLOAD_FOLDER = os.path.join(os.getenv('FLASK_INSTANCE_PATH', '/tmp'), 'uploads')
    PROCESSED_FOLDER = os.path.join(os.getenv('FLASK_INSTANCE_PATH', '/tmp'), 'processed')
    MODEL_PATH = os.path.join(os.getenv('FLASK_INSTANCE_PATH', '/tmp'), 'big-bird')
    DATABASE  = os.path.join(os.getenv('FLASK_INSTANCE_PATH', '/tmp'), 'flaskr.sqlite')



class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    DATABASE = 'postgresql://user:password@db:5432/mydb'
    CELERY = {
        'broker_url': 'redis://redis:6379/0',
        'result_backend': 'redis://redis:6379/0',
        'task_track_started': True,
        'task_ignore_result': False,
        'result_serializer': 'json',
    }
    SECRET_KEY = os.getenv('SECRET_KEY')  # Fetch from environment
    UPLOAD_FOLDER = os.path.join(os.getenv('FLASK_INSTANCE_PATH', '/tmp'), 'uploads')
    PROCESSED_FOLDER = os.path.join(os.getenv('FLASK_INSTANCE_PATH', '/tmp'), 'processed')


class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    DATABASE = 'sqlite:///test_db.sqlite'
