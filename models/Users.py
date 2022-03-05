
from manage import db
from sqlalchemy.orm import validates
from sqlalchemy.schema import CheckConstraint
from werkzeug.security import check_password_hash


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String, nullable=False, unique=True)
    password_hash = db.Column(db.String, nullable=False, unique=True)
    session_token = db.Column(db.String, unique=True, nullable=True)
    session_id = db.Column(db.String, unique=True, nullable=True)

    def string_length_validation(self, string_value):
        if len(string_value) < 8:
            raise ValueError("Value too short")
        elif len(string_value) > 28:
            raise ValueError("Value too long")

        return string_value

    @validates("username")
    def username_validation(self, key, some_string):
        return self.string_length_validation(some_string)

    __table_args__ = (
        CheckConstraint('char_length(password_hash) > 8',
                        name='password_hash'),
        CheckConstraint('char_length(username) > 8',
                        name='username')
    )

    def __init__(self, username, password_hash, session_token, session_id):
        self.username = username
        self.password_hash = password_hash
        self.session_token = session_token
        self.session_id = session_id

    def verify_password(self, pwd):
        return check_password_hash(self.password_hash, pwd)
