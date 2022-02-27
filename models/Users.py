
from manage import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), unique=True, nullable=False)
    first_name = db.Column(db.String, nullable=False)

    # password = db.Column(db.String(128), unique=True, nullable=False)
    # session_token = db.Column(db.String(128), unique=True, nullable=False)

    def __init__(self, email, first_name):
        self.email = email
        self.first_name = first_name
        # self.password = password
        # self.session_token = session_token
