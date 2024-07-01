import os

from flask import Flask
from flask_restful import Resource, Api
from celery import Celery, Task

# Change redis url to your redis server when deploying
# Setup redis server on deploying
def celery_init_app(app: Flask):
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(app.name, task_cls=FlaskTask)
    celery_app.config_from_object(app.config["CELERY"])
    celery_app.set_default()

    TaskBase = celery_app.Task
    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery_app.Task = ContextTask


    app.extensions["celery"] = celery_app
    return celery_app


def create_app(test_config=None):

    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )
      
    app.config['UPLOAD_FOLDER'] = os.path.join(app.instance_path, 'uploads')
    app.config["PROCESSED_FOLDER"] = os.path.join(app.instance_path, 'processed')
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
    app.config['CORS_HEADER'] = 'application/json'
    app.config.from_mapping(
    CELERY=dict(
        broker_url='redis://localhost:6379/0',
        result_backend='redis://localhost:6379/0',
        task_ignore_result=True,
    ),
)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from routes import main
    app.register_blueprint(main)

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'
    
    import db
    db.init_app(app)

    celery_init_app(app)
    import tasks
    return app


app = Flask(__name__)

