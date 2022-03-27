from flask import Blueprint
from dal.User_dal import UserDal
from flask import request, jsonify, Response
from flask_jwt_extended import get_jwt
from flask_jwt_extended import jwt_required


auth_controller = Blueprint("auth", __name__)


@auth_controller.route("/protected")
@jwt_required()
def protected():
    return jsonify(foo="bar")


@auth_controller.route("/auth/login", methods=["POST"])
def login():
    username = request.json['username']
    password = request.json['password']
    session_token = UserDal.login_user(username, password)

    return jsonify(token=session_token)


@auth_controller.route("/auth/sign_up", methods=["POST"])
def sign_up():
    try:
        username = request.json["username"]
        password = request.json["password"]
        session_token = UserDal.create_new_user(
            username=username, password=password)

        return jsonify(token=session_token)
    except Exception as exception:
        error_response = Response(status=404)
        error_response.set_data("invalid signup")
        return error_response


@auth_controller.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    jwt = get_jwt()
    jti = jwt["jti"]
    UserDal.logout_user(jti)
    return jsonify({"msg": "logout successful"})
