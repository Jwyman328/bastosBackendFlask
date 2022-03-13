import pytest


from manage import create_app

from manage import db
from models.Articles import Article
from models.Categories import Category
from models.Users import User
from fixtures.user_fixtures import valid_user_data
from fixtures.article_fixtures import article_1_fixture, article_2_fixture
from fixtures.category_fixtures import category_economics_fixture, category_history_fixture, category_horror_fixture


@pytest.fixture(scope="function")
def log_test_start():
    return "hi bob"


# TESTDB = 'test_project.db'
# TESTDB_PATH = "{}".format(TESTDB)
# TEST_DATABASE_URI = 'postgresql://' + TESTDB_PATH

# print("ahh", TEST_DATABASE_URI)


@pytest.fixture(scope="session")
def test_client(request):
    test_app = create_app('flask_test.cfg')

    def teardown():
        print("teardown run")

    request.addfinalizer(teardown)

    # Create a test client using the Flask application configured for testing
    with test_app.test_client() as testing_client:
        # Establish an application context
        with test_app.app_context() as app_context:
            yield testing_client  # this is where the testing happens!
            app_context.push()


@pytest.fixture(scope="session")
def init_db(test_client, request):
    """session-wide test database."""

    def teardown():
        db.drop_all()

    db.create_all()

    request.addfinalizer(teardown)
    db.session.commit()

    return db


@pytest.fixture(scope="function")
def populate_db_with_valid_user(test_client, init_db, request):
    db = init_db
    valid_user = User(
        username=valid_user_data["username"], password=valid_user_data["password"])

    db.session.add(valid_user)
    db.session.commit()

    def teardown():
        User.query.filter(User.id == valid_user.id).delete()
        db.session.commit()

    request.addfinalizer(teardown)

    return valid_user


@pytest.fixture(scope="function")
def populate_db_with_articles_and_categories(test_client, init_db, request):
    db = init_db

    horror = Category(category=category_horror_fixture)
    economics = Category(category=category_economics_fixture)
    history = Category(category=category_history_fixture)

    article_1 = Article(url=article_1_fixture["url"], imageUrl=article_1_fixture["imageUrl"],
                        title=article_1_fixture["title"])

    article_2 = Article(url=article_2_fixture["url"], imageUrl=article_2_fixture["imageUrl"],
                        title=article_2_fixture["title"])
    db.session.add_all([article_2, article_1, horror, history,  economics])
    db.session.commit()
    article_1.categories.extend([horror, economics])
    article_2.categories.extend([horror, economics, history])
    db.session.commit()

    def teardown():
        all_articles = Article.query.all()
        all_categories = Category.query.all()
        for article_item in all_articles:
            db.session.delete(article_item)
            db.session.commit()

        for category_item in all_categories:
            db.session.delete(category_item)
            db.session.commit()

    request.addfinalizer(teardown)
    return {"categories": [horror, economics, history], "articles": [article_1, article_2]}


@pytest.fixture(scope="function")
def drop_all_users(test_client, init_db):
    User.query.delete()
    init_db.session.commit()
