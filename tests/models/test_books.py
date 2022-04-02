from models.Books import Book
from models.Users import User
from models.Categories import Category
from fixtures.book_fixtures import creadores_de_riqueza, fundamentos_de_la_libertad
from fixtures.category_fixtures import category_economics_fixture, category_history_fixture


def test_books(test_client):
    """Test you can create books and it will contain appropriate properties."""
    fundamentos_de_la_libertad_instance = Book(**fundamentos_de_la_libertad)
    first_category = Category(category=category_economics_fixture)
    fundamentos_de_la_libertad_instance.catagories.append(first_category)

    # asset Book to category relationship
    category_in_the_book = fundamentos_de_la_libertad_instance.catagories[0].category
    assert category_in_the_book == first_category.category

    # assert Category to book relationship
    fundamentos_book_title_from_first_category = first_category.book[0].title
    assert fundamentos_book_title_from_first_category == fundamentos_de_la_libertad_instance.title

    # assert Book instance create with title
    assert fundamentos_de_la_libertad_instance.title == fundamentos_de_la_libertad["title"]

    # add another Category and assert two now exist
    second_category = Category(category=category_history_fixture)
    fundamentos_de_la_libertad_instance.catagories.append(second_category)

    assert len(fundamentos_de_la_libertad_instance.catagories) == 2


def test_books_json_methods(test_client):
    """Test category is returned as json with no backref to Book object"""
    fundamentos_de_la_libertad_instance = Book(**fundamentos_de_la_libertad)
    first_category = Category(category=category_economics_fixture)
    fundamentos_de_la_libertad_instance.catagories.append(first_category)

    json_book = fundamentos_de_la_libertad_instance.get_books_and_related_categories_as_jsonable()
    assert json_book["catagories"] == [
        {"category": category_economics_fixture}]


def test_has_been_read_by_user(test_client):
    username = "MyNameIsTheUSer"
    password = "randomHashfsdaffds"

    new_user = User(username=username, password=password)
    new_user.id = 1
    new_book = Book(**creadores_de_riqueza)
    new_user.read_books.append(new_book)

    assert new_book.has_been_read_by_user(new_user.id) == True
    assert new_book.has_been_read_by_user("non user") == False
