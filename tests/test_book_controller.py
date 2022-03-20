import json
from tests.helpers.helpers import create_authentication_header
import unittest

def test_user_read_books_are_marked_as_read(test_client,  valid_user_has_read_first_book,):
    valid_user_session_token = valid_user_has_read_first_book["user"].session_token
    valid_user_request_headers = create_authentication_header(valid_user_session_token)
    response = test_client.get("/books", headers=valid_user_request_headers)
    # convert json data to python
    response_data_as_python_dict = json.loads(response.get_data(as_text=True))


    has_user_read_first_book = response_data_as_python_dict[0]["hasUserReadBook"]
    has_user_read_second_book = response_data_as_python_dict[1]["hasUserReadBook"]

    assert has_user_read_first_book == True 
    assert has_user_read_second_book == False 

def test_book_controller_returns_all_books_as_json(test_client, populate_db_with_valid_user, populate_db_with_books_and_categories):
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


def test_mark_book_as_read(test_client, populate_db_with_valid_user, populate_db_with_books_and_categories):
    valid_user = populate_db_with_valid_user
    valid_user_session_token = valid_user.session_token
    valid_user_request_headers = create_authentication_header(valid_user_session_token)
    un_read_book = populate_db_with_books_and_categories["books"][0]
    assert valid_user.read_books == []
    book_data = {"bookId": un_read_book.id }
    response = test_client.post("/books/read", headers=valid_user_request_headers, data=json.dumps(book_data))
    # should return 201
    assert response.status == "201 CREATED"

    # next request should return one book 
    response = test_client.get("/books", headers=valid_user_request_headers)
    response_data_as_python_dict = json.loads(response.get_data(as_text=True))
    print("response_data_as_python_dict", response_data_as_python_dict)
    #loop through all books and verify the bookId that was marked as read is.
    for book in response_data_as_python_dict:
        print("book id", book)
        if book["id"] == un_read_book.id:
            assert book["hasUserReadBook"] == True 
        else:
            assert book["hasUserReadBook"] == False
    


def test_mark_book_as_unread(test_client, valid_user_has_read_first_book):
    valid_user = valid_user_has_read_first_book["user"]
    valid_user_session_token = valid_user.session_token
    valid_user_request_headers = create_authentication_header(valid_user_session_token)
    read_book = valid_user_has_read_first_book["book"]

    # User has marked one book as read
    assert len(valid_user.read_books) == 1


    book_data = {"id": read_book.id }
    response = test_client.delete("/books/read", headers=valid_user_request_headers, query_string=book_data)
    # should return 201
    assert response.status == "204 NO CONTENT"

    response = test_client.get("/books", headers=valid_user_request_headers)
    response_data_as_python_dict = json.loads(response.get_data(as_text=True))
    #loop through all books are now unread.
    for book in response_data_as_python_dict:
        assert book["hasUserReadBook"] == False


def test_mark_single_book_as_unread_when_user_has_two_books_marked_as_read(test_client, valid_user_has_read_two_books):
    valid_user = valid_user_has_read_two_books["user"]
    valid_user_session_token = valid_user.session_token
    valid_user_request_headers = create_authentication_header(valid_user_session_token)
    read_books = valid_user_has_read_two_books["books"]

    # User has marked one book as read
    assert len(valid_user.read_books) == 2

    book_to_be_marked_as_unread = read_books[0]
    book_data = {"id": book_to_be_marked_as_unread.id }
    response = test_client.delete("/books/read", headers=valid_user_request_headers, query_string=book_data)
    # should return 201
    assert response.status == "204 NO CONTENT"

    response = test_client.get("/books", headers=valid_user_request_headers)
    response_data_as_python_dict = json.loads(response.get_data(as_text=True))
    
    #loop through all books and unread book should be False and other book still True
    for book in response_data_as_python_dict:
        if book["id"] == book_to_be_marked_as_unread.id:
            assert book["hasUserReadBook"] == False
        else:
            assert book["hasUserReadBook"] == True
