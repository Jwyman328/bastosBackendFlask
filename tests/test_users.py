import pytest
from models.Users import User


def test_user_model(test_client):
    username = "MyNameIsTheUSer"
    password = "randomHashfsdaffds"

    new_user = User(username=username, password=password)

    assert new_user.session_id != None
    assert new_user.username == username
    assert new_user.password_hash != password
    assert new_user.session_token != None

# test empty name throws error on string validation


def test_username_string_min_len_validation():
    username = ""
    password = "randomHashfsdaffds"

    with pytest.raises(Exception, match="Value too short") as e:
        User(username=username, password=password)
    assert str(e.value) == "Value too short"


def test_username_string_max_len_validation():
    username = "afdfadsfsdfsadfasfasdfasdkfsadfka;ldfk;lasdkf;alsdkfafffffff;lsdfk;asfka;ldsfkas;dlfkasflkas;fkasd;lf"
    password = "randomHashfsdaffds"

    with pytest.raises(Exception) as e:
        User(username=username, password=password)
    assert str(e.value) == "Value too long"
