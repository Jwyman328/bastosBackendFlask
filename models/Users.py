
from manage import db
from sqlalchemy.orm import validates
from sqlalchemy.schema import CheckConstraint
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token, get_jti
from werkzeug.security import generate_password_hash
from models.relationships.user_read_book import user_read_books
from models.relationships.user_watched_videos import user_watched_videos

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String, nullable=False, unique=True)
    password_hash = db.Column(db.String, nullable=False, unique=True)
    session_token = db.Column(db.String, unique=True, nullable=True)
    session_id = db.Column(db.String, unique=True, nullable=True)
    read_books = db.relationship(
        "Book", secondary=user_read_books, backref="read_by_users", lazy=False)
    watched_videos =  db.relationship(
        "Video", secondary=user_watched_videos, backref="users_that_have_watched_this_video", lazy=False)

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

    def __init__(self, username, password):
        access_token = create_access_token(identity=username)
        jti = get_jti(access_token)
        hashed_password = generate_password_hash(password)

        self.username = username
        self.password_hash = hashed_password
        self.session_token = access_token
        self.session_id = jti

    def verify_password(self, pwd):
        return check_password_hash(self.password_hash, pwd)