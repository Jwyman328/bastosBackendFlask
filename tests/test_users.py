import pytest
from models.Users import User


def test_user_model():
    session_id = "this is seshid"
    username = "MyNameIsTheUSer"
    password_hash = "randomHashfsdaffds"
    session_token = "thisisasessiontokendoyoulikeit"

    new_user = User(username=username, password_hash=password_hash,
                    session_token=session_token, session_id=session_id)

    assert new_user.session_id == session_id
    assert new_user.username == username
    assert new_user.password_hash == password_hash
    assert new_user.session_token == session_token

# test empty name throws error on string validation


def test_username_string_min_len_validation():
    session_id = "this is seshid"
    username = ""
    password_hash = "randomHashfsdaffds"
    session_token = "thisisasessiontokendoyoulikeit"

    with pytest.raises(Exception, match="Value too short") as e:
        new_user = User(username=username, password_hash=password_hash,
                        session_token=session_token, session_id=session_id)
    assert str(e.value) == "Value too short"


def test_username_string_max_len_validation():
    session_id = "this is seshid"
    username = "afdfadsfsdfsadfasfasdfasdkfsadfka;ldfk;lasdkf;alsdkfafffffff;lsdfk;asfka;ldsfkas;dlfkasflkas;fkasd;lf"
    password_hash = "randomHashfsdaffds"
    session_token = "thisisasessiontokendoyoulikeit"

    with pytest.raises(Exception) as e:
        new_user = User(username=username, password_hash=password_hash,
                        session_token=session_token, session_id=session_id)
    assert str(e.value) == "Value too long"
