from tests.conftest import test_client, init_db
from manage import create_app

# one way to test the app without fixtures


def test_root_get():
    flask_client = create_app('flask_test.cfg')
    with flask_client.test_client() as test_client:

        print('test db', init_db)
        response = test_client.get('/')
        assert response.data == b"hello world"
        assert response.status == '200 OK'


# testing hte app with  fixtures
def test_root_get_with_db_fixture(test_client, init_db):

    response = test_client.get('/')
    assert response.data == b"hello world"
    assert response.status == '200 OK'
