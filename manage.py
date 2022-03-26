# all the imports
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from datetime import timedelta

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
    init_auth_jwt(app)
    init_blueprints(app)

    return app


def init_blueprints(app):
    from controllers.auth import auth_controller
    from controllers.root import root_blueprint
    from controllers.articles import article_controller
    from controllers.books import books_controller
    from controllers.videos import videos_controller

    app.register_blueprint(auth_controller)
    app.register_blueprint(article_controller)
    app.register_blueprint(root_blueprint)
    app.register_blueprint(books_controller)
    app.register_blueprint(videos_controller)


def init_auth_jwt(app):
    from models.Users import User

    jwt = JWTManager(app)

    # Register a callback function that takes whatever object is passed in as the
    # identity when creating JWTs and converts it to a JSON serializable format.
    # don't really think this does much as of right now

    @jwt.user_identity_loader
    def user_identity_lookup(user):
        return user

    # Register a callback function that loads a user from your database whenever
    # a protected route is accessed. This should return any python object on a
    # successful lookup, or None if the lookup failed for any reason (for example
    # if the user has been deleted from the database).

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        try:
            user_identifying_data_stored_in_jwt = jwt_data["jti"]
            return User.query.filter_by(session_id=user_identifying_data_stored_in_jwt).one_or_none()
        except Exception as error:
            raise Exception("invalid user")
