import pytest
from models.Users import User
from models.Books import Book
from fixtures.book_fixtures import creadores_de_riqueza


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


def test_user_read_books():
    """Test the books added to the users have read list can be referenced through the user and backref through book class"""
    username = "MyNameIsTheUSer"
    password = "randomHashfsdaffds"

    new_user = User(username=username, password=password)
    new_book = Book(**creadores_de_riqueza)
    new_user.read_books.append(new_book)

    assert new_user.read_books[0].title == new_book.title

    # assert you can access the user from the book back ref
    all_user_that_have_read_the_book = new_book.read_by_users
    assert len(all_user_that_have_read_the_book) == 1
    assert all_user_that_have_read_the_book[0].username == new_user.username
