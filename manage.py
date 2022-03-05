from datetime import timedelta
from flask.cli import FlaskGroup
# all the imports
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager


# app = Flask(__name__)  # create the application instance :)
# app.config.from_object(__name__)  # load config from this file , flaskr.py
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

# If true this will only allow the cookies that contain your JWTs to be sent
# over https. In production, this should always be set to True
def set_cookie_secure():
    env = os.getenv("FLASK_ENV")
    if (env == 'development'):
        return False
    else:
        return True


basedir = os.path.abspath(os.path.dirname(__file__))


app = Flask(__name__)
app.config.from_object(__name__)

# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET")  # Change this!
app.config["JWT_COOKIE_SECURE"] = set_cookie_secure()
app.config["JWT_TOKEN_LOCATION"] = ["headers"]
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)


app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL", "sqlite://")
print('database uri', app.config['SQLALCHEMY_DATABASE_URI'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
jwt = JWTManager(app)
