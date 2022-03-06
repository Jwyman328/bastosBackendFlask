import pytest

from manage import create_app
from controllers.auth import auth_controller
from controllers.root import root_blueprint


@pytest.fixture(scope="function")
def log_test_start():
    return "hi bob"


@pytest.fixture(scope="function")
def test_client():
    test_app = create_app(testing=True)
    test_app.register_blueprint(auth_controller)
    test_app.register_blueprint(root_blueprint)
    with test_app.test_client() as test_client_app:
        return test_client_app
        print('run after')
