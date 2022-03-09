
from models.Users import User
from manage import db
from flask_jwt_extended import create_access_token, get_jti
from flask import jsonify
from werkzeug.security import generate_password_hash


class UserDal():

    @staticmethod
    def create_new_user(username, password):
        access_token = create_access_token(identity=username)
        jti = get_jti(access_token)
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password_hash=hashed_password,
                        session_token=access_token, session_id=jti)
        db.session.add(new_user)
        db.session.commit()

        return access_token

    @staticmethod
    def login_user(username, password):
        # find user by username
        user = User.query.filter_by(username=username).first()
        if (user and user.verify_password(password)):
            new_access_token = create_access_token(identity=username)
            return new_access_token
        else:
            raise Exception("User login error")

    @staticmethod
    def logout_user(jti):
        try:
            user = User.query.filter_by(session_id=jti).update({
                "session_token": None, "session_id": None})
            db.session.commit()
            return "success"
        except:
            raise Exception("User logout error")
