from datetime import timedelta
from flask.cli import FlaskGroup
# all the imports
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager


db = SQLAlchemy()

# If true this will only allow the cookies that contain your JWTs to be sent
# over https. In production, this should always be set to True
def set_cookie_secure():
    env = os.getenv("FLASK_ENV")
    if (env == 'development'):
        return False
    else:
        return True


basedir = os.path.abspath(os.path.dirname(__file__))


def create_app(config_filename=None):
    app = Flask(__name__)
    app.config.from_pyfile(config_filename)

    # Setup the Flask-JWT-Extended extension
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET")  # Change this!
    app.config["JWT_COOKIE_SECURE"] = set_cookie_secure()
    app.config["JWT_TOKEN_LOCATION"] = ["headers"]
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)

    db.init_app(app)
    init_blueprints(app)

    return app


def init_blueprints(app):
    from controllers.auth import auth_controller
    from controllers.root import root_blueprint
    app.register_blueprint(auth_controller)

    app.register_blueprint(root_blueprint)
