import os

from flask import Flask
from celery import Celery, Task
from flaskr.model import init_model_and_tokenizer
from flaskr.config import Config, DevelopmentConfig, ProductionConfig, TestingConfig

# Change redis url to your redis server when deploying
# Setup redis server on deploying
# Set FLASK_INSTANCE_PATH environment variable to the path of the instance folder

def celery_init_app(app: Flask):
    class ContextTask(Task):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return super().__call__(*args, **kwargs)

    celery_app = Celery(app.name, task_cls=ContextTask)
    celery_app.config_from_object(app.config["CELERY"])
    celery_app.set_default()
    celery_app.Task = ContextTask


    app.extensions["celery"] = celery_app
    return celery_app


def create_app():

    print("STARTING APP")

    app = Flask(__name__, instance_relative_config=True)

    flask_env = os.getenv('FLASK_ENV', 'development')

    if flask_env == 'development':
        app.config.from_object(DevelopmentConfig)

        init_model_and_tokenizer(app.config["MODEL_PATH"])

        try:
            if not os.path.exists(app.config['UPLOAD_FOLDER']):
                os.makedirs(app.config['UPLOAD_FOLDER'])
            if not os.path.exists(app.config['PROCESSED_FOLDER']):
                os.makedirs(app.config['PROCESSED_FOLDER'])
            if not os.path.exists(app.config['MODEL_PATH']):
                os.makedirs(app.config['MODEL_PATH'])
                
        except OSError:
            print("Error creating directories")


    elif flask_env == 'production':
        app.config.from_object(ProductionConfig)
        
        try:
            os.makedirs(app.instance_path)
        
        except OSError:
            pass
    
    elif flask_env == 'testing': # Configure for testing later
        app.config.from_object(TestingConfig)
        init_model_and_tokenizer(app.config["MODEL_PATH"])
        
        try:
            os.makedirs(app.instance_path)
        
        except OSError:
            pass


    from flaskr.routes import epub
    app.register_blueprint(epub)

    
    from flaskr.db import init_app
    init_app(app)

    celery_init_app(app)
    
    return app


if __name__ == "__main__":
    app = create_app()


