
from dal.create_new_user import create_new_user
from manage import app, db, jwt
from models.Users import User
from flask import request, jsonify, abort, Response
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from werkzeug.security import check_password_hash


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
    identity = jwt_data["sub"]
    return User.query.filter_by(id=identity).one_or_none()


@app.get('/')
def main_fun():
    return User.query.all()[0].username


@app.route("/auth/login", methods=["GET"])
def login():
    # get username, password
    # check_password_hash
    username = request.data['username']
    password = request.data['password']
    return {"token": "123"}
    # save user then return a token


@app.route("/auth/sign_up", methods=["POST"])
def sign_up():
    try:
        username = request.json["username"]
        password = request.json["password"]
        session_token = create_new_user(username=username, password=password)

        return jsonify(access_token=session_token)
    except Exception as exception:
        error_response = Response(status=404)
        error_response.set_data("invalid signup")
        return error_response


if __name__ == "__main__":
    app.run(
        debug=True,
        host='0.0.0.0',
        port=5000
    )
