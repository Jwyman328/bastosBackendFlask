import pytest
import os

from manage import create_app

from manage import db


@pytest.fixture(scope="function")
def log_test_start():
    return "hi bob"


TESTDB = 'test_project.db'
TESTDB_PATH = "{}".format(TESTDB)
TEST_DATABASE_URI = 'postgresql://' + TESTDB_PATH

print("ahh", TEST_DATABASE_URI)


@pytest.fixture(scope="session")
def test_client(request):
    test_app = create_app('flask_test.cfg')

    def teardown():
        print("teardown run")

    request.addfinalizer(teardown)

    # Create a test client using the Flask application configured for testing
    with test_app.test_client() as testing_client:
        # Establish an application context
        with test_app.app_context():
            yield testing_client  # this is where the testing happens!


@pytest.fixture(scope="session")
def init_db(test_client, request):
    """session-wide test database."""

    def teardown():
        db.drop_all()

    db.create_all()

    request.addfinalizer(teardown)
    db.session.commit()

    # return db

