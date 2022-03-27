import json

from flask import jsonify
from manage import create_app
from models.Users import User
from tests.conftest import log_test_start, test_client, populate_db_with_valid_user
from fixtures.user_fixtures import valid_user_data


def test_login(test_client, populate_db_with_valid_user):
    login_data = {"username": valid_user_data["username"],
                  "password": valid_user_data["password"]}
    response = test_client.post('/auth/login', data=json.dumps(login_data),
                                headers={"Content-Type": "application/json"},)

    data = json.loads(response.get_data(as_text=True))

    assert data["token"] == populate_db_with_valid_user.session_token


# returns success, adds user to database, and returns access_token
def test_signup(test_client, init_db):
    # user database starts empty
    empty_db = User.query.all()
    assert empty_db == []

    login_data = {"username": valid_user_data["username"],
                  "password": valid_user_data["password"]}
    response = test_client.post('/auth/sign_up', data=json.dumps(login_data),
                                headers={"Content-Type": "application/json"},)

    data = json.loads(response.get_data(as_text=True))
    assert data["access_token"] == User.query.first().session_token


def test_logout(test_client, drop_all_users, populate_db_with_valid_user):
    # log should clear current user token data from db, respondes with logout successful

    user_token = populate_db_with_valid_user.session_token
    response = test_client.post(
        '/logout', headers={"Content-Type": "application/json", "Authorization": f"Bearer {user_token}"},)
    data = json.loads(response.get_data(as_text=True))
    assert data["msg"] == 'logout successful'

    logged_out_user = User.query.filter_by(
        username=populate_db_with_valid_user.username).first()

    assert logged_out_user.session_token == None
    assert logged_out_user.session_id == None
