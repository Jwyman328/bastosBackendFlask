import json
from tests.helpers.helpers import create_authentication_header
import unittest

def test_user_read_books_are_marked_as_read(test_client,  valid_user_has_read_first_book,):
    valid_user_session_token = valid_user_has_read_first_book.session_token
    valid_user_request_headers = create_authentication_header(valid_user_session_token)
    response = test_client.get("/books", headers=valid_user_request_headers)
    # convert json data to python
    response_data_as_python_dict = json.loads(response.get_data(as_text=True))


    has_user_read_first_book = response_data_as_python_dict[0]["hasUserReadBook"]
    has_user_read_second_book = response_data_as_python_dict[1]["hasUserReadBook"]

    assert has_user_read_first_book == True 
    assert has_user_read_second_book == False 

def test_book_controller_returns_all_books_as_json(test_client, populate_db_with_valid_user, populate_db_with_books_and_categories,):
    valid_user_session_token = populate_db_with_valid_user.session_token
    valid_user_request_headers = create_authentication_header(valid_user_session_token)
    response = test_client.get("/books", headers=valid_user_request_headers)
    # convert json data to python
    response_data_as_python_dict = json.loads(response.get_data(as_text=True))

    first_book_title_from_response = response_data_as_python_dict[0]["title"]

    # get book data that initiated the db
    all_books_instances = populate_db_with_books_and_categories["books"]
    first_book_title_from_init_db_methods = all_books_instances[0].title

    assert first_book_title_from_response == first_book_title_from_init_db_methods

    # assert contains two books
    assert len(response_data_as_python_dict) == 2

    # assert first book in response has two categories as dictionary
    first_book_categories = response_data_as_python_dict[0]["catagories"]
    first_book_categories_from_init_db_methods = all_books_instances[0].get_json_categories_without_book_backref(
    )
    unittest.TestCase.assertCountEqual(None, first_book_categories, first_book_categories_from_init_db_methods)

