from flask.cli import FlaskGroup
# all the imports
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


# app = Flask(__name__)  # create the application instance :)
# app.config.from_object(__name__)  # load config from this file , flaskr.py
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

basedir = os.path.abspath(os.path.dirname(__file__))


app = Flask(__name__)
app.config.from_object(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL", "sqlite://")
print('database uri', app.config['SQLALCHEMY_DATABASE_URI'])
# app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://hello_flask:hello_flask@db:5432/hello_flask_dev"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
