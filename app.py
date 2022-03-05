
from manage import app, db
from models.Users import User
from flask import request, jsonify


@app.get('/')
def main_fun():
    return "hello"
    # return User.query.all()[0].email


@app.route("/auth/login", methods=["GET"])
def login():
    # get username, password
    username = request.form['username']
    password = request.password['password']
    return {"token": "123"}
    # save user then return a token

# @app.route("/auth/sign_up", methods=["POST"])


@app.route("/auth/sign_up", methods=["POST"])
def sign_up():
    # get username, password
    try:
        print("got the reqeust", request)
        # username = request.form['username']
        # password = request.password['password']
        return jsonify({"token": "123"})
    except:
        print("Exception thrown. x does not exist.")
        return "hello world"


if __name__ == "__main__":
    app.run(
        debug=True,
        host='0.0.0.0',
        port=5000
    )
