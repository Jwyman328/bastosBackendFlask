

from datetime import datetime, timedelta
from dal.User_dal import UserDal
from manage import create_app, jwt
from models.Users import User
from flask import request, jsonify, abort, Response
from flask_jwt_extended import create_access_token, get_jwt
from flask_jwt_extended import get_jwt_identity, get_jti
from flask_jwt_extended import jwt_required
from werkzeug.security import check_password_hash
from flask_jwt_extended import JWTManager


app = create_app('flask.cfg')
jwt = JWTManager(app)


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
    try:
        user_identifying_data_stored_in_jwt = jwt_data["jti"]
        return User.query.filter_by(session_id=user_identifying_data_stored_in_jwt).one_or_none()
    except Exception as error:
        raise Exception("invalid user")

# Using an `after_request` callback, we refresh any token that is within 30
# minutes of expiring. Change the timedeltas to match the needs of your application.
# @app.after_request
# def refresh_expiring_jwts(response):
#     try:
#         print("hello world")
#         exp_timestamp = get_jwt()["exp"]
#         now = datetime.now(timezoe.utc)
#         target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
#         if target_timestamp > exp_timestamp:
#             access_token = create_access_token(identity=get_jwt_identity())
#             set_access_cookies(response, access_token)
#         return response
#     except (RuntimeError, KeyError):
#         # Case where there is not a valid JWT. Just return the original respone
#         return response


@app.route("/protected")
@jwt_required()
def protected():
    return jsonify(foo="bar")



if __name__ == "__main__":
    app.run(
        debug=True,
        host='0.0.0.0',
        port=5000
    )
