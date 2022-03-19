
from models.Users import User
from manage import db
from flask_jwt_extended import create_access_token, get_jti


class UserDal():

    @staticmethod
    def create_new_user(username, password):
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()

        return new_user.session_token

    @staticmethod
    def login_user(username, password):
        user = User.query.filter_by(username=username).first()

        if (user and user.verify_password(password)):
            new_access_token = create_access_token(identity=username)
            jti = get_jti(new_access_token)
            # save new token in db
            setattr(user, "session_token", new_access_token)
            setattr(user, "session_id", jti)

            return new_access_token
        else:
            raise Exception("User login error")

    @staticmethod
    def logout_user(jti):
        try:
            User.query.filter_by(session_id=jti).update({
                "session_token": None, "session_id": None})
            db.session.commit()
            return "success"
        except:
            raise Exception("User logout error")

    def get_user_by_jti(jti):
        return  User.query.filter_by(session_id=jti).first()
