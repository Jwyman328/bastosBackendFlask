

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


if __name__ == "__main__":
    app.run(
        debug=True,
        host='0.0.0.0',
        port=5000
    )
