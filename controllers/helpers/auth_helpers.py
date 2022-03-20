from dal.User_dal import UserDal
from flask_jwt_extended import get_jwt

def get_current_user_by_jwt():
    jwt = get_jwt()
    jti = jwt["jti"]
    current_user = UserDal.get_user_by_jti(jti)
    return current_user