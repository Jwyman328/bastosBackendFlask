from models.Users import User
from manage import app, db, jwt
from flask_jwt_extended import create_access_token
from flask import jsonify
from werkzeug.security import generate_password_hash


def create_new_user(username, password):
    access_token = create_access_token(identity=username)
    hashed_password = generate_password_hash(password)
    new_user = User(username=username, password_hash=hashed_password,
                    session_token=access_token)
    db.session.add(new_user)
    db.session.commit()

    return access_token
