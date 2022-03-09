from manage import create_app
from tests.conftest import log_test_start, test_client


# def test_auth(log_test_start):
#     test_app = create_app()
#     with test_app.test_client() as test_client:
#         print("log_test_start", log_test_start)
#         assert log_test_start == "hi bob"
#         response = test_client.get('/')
#         assert response.data == "hello world"
#         assert response.status == 200


# def test_auth_get(test_client):
#     response = test_client.get('/')
#     assert response.data == "hello world"
#     assert response.status == 200


# def test_auth_get_raw():
#     test_app = create_app(testing=True)
#     with test_app.test_client() as test_client_app:
#         response = test_client_app.get('/protected')
#         assert response.status == 200
