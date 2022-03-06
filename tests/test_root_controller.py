from manage import create_app
from tests.conftest import log_test_start, test_client


def test_root_get(test_client):
    response = test_client.get('/')
    assert response.data == b"hello world"
    assert response.status == '200 OK'
