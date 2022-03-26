import pytest


from manage import create_app

from manage import db
from models.Articles import Article
from models.Categories import Category
from models.Users import User
from models.Books import Book
from models.Videos import Video
from models.Notes import Note
from fixtures.user_fixtures import valid_user_data
from fixtures.article_fixtures import article_1_fixture, article_2_fixture
from fixtures.category_fixtures import category_economics_fixture, category_history_fixture, category_horror_fixture
from fixtures.book_fixtures import creadores_de_riqueza, fundamentos_de_la_libertad
from fixtures.video_fixtures import video_fixture, video_fixture_2
from fixtures.note_fixtures import note_fixture_one

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
    db.session().expire_on_commit = False

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
def populate_db_with_books_and_categories(test_client, init_db, request):
    db = init_db

    horror = Category(category=category_horror_fixture)
    economics = Category(category=category_economics_fixture)
    history = Category(category=category_history_fixture)

    book_1 = Book(**creadores_de_riqueza)
    book_2 = Book(**fundamentos_de_la_libertad)
    db.session.add_all([book_1, book_2, horror, history,  economics])
    db.session.commit()
    book_1.catagories.extend([horror, economics])
    book_2.catagories.extend([horror, economics, history])
    db.session.commit()

    def teardown():
        all_books = Book.query.all()
        all_categories = Category.query.all()
        for book_item in all_books:
            db.session.delete(book_item)
            db.session.commit()

        for category_item in all_categories:
            db.session.delete(category_item)
            db.session.commit()

    request.addfinalizer(teardown)
    return {"categories": [horror, economics, history], "books": [book_1, book_2]}

@pytest.fixture(scope="function")
def valid_user_has_read_first_book(init_db, populate_db_with_valid_user, populate_db_with_books_and_categories, request):
    db = init_db

    all_books = populate_db_with_books_and_categories["books"]
    valid_user = populate_db_with_valid_user
    valid_user.read_books.append(all_books[0])
    db.session.commit()

    return {"user":valid_user, "book": all_books[0]}

@pytest.fixture(scope="function")
def valid_user_has_read_two_books(init_db, populate_db_with_valid_user, populate_db_with_books_and_categories, request):
    db = init_db

    all_books = populate_db_with_books_and_categories["books"]
    valid_user = populate_db_with_valid_user
    valid_user.read_books.append(all_books[0])
    valid_user.read_books.append(all_books[1])
    db.session.commit()

    return {"user":valid_user, "books": all_books}

@pytest.fixture(scope="function")
def populate_db_with_videos_and_categories(test_client, init_db, request):
    db = init_db

    horror = Category(category=category_horror_fixture)
    economics = Category(category=category_economics_fixture)
    history = Category(category=category_history_fixture)

    
    video_1 = Video(title=video_fixture["title"], image=video_fixture["image"], noteCount=video_fixture["noteCount"], year=video_fixture["year"], videoUrl=video_fixture["videoUrl"])
    video_2 = Video(title=video_fixture_2["title"], image=video_fixture_2["image"], noteCount=video_fixture_2["noteCount"], year=video_fixture_2["year"], videoUrl=video_fixture_2["videoUrl"])

    db.session.add_all([video_1, horror, history,  economics, video_2])
    db.session.commit()
    video_1.categories.extend([horror, economics])
    video_2.categories.extend([history])
    db.session.commit()

    def teardown():
        all_videos = Video.query.all()
        all_categories = Category.query.all()
        for book_item in all_videos:
            db.session.delete(book_item)
            db.session.commit()

        for category_item in all_categories:
            db.session.delete(category_item)
            db.session.commit()

    request.addfinalizer(teardown)
    return {"categories": [horror, economics, history], "videos": [video_1, video_2]}

@pytest.fixture(scope="function")
def populate_db_with_videos_and_notes(init_db, populate_db_with_videos_and_categories, request):
    db = init_db
    videos = populate_db_with_videos_and_categories["videos"]

    new_note_for_video_1 = Note(**note_fixture_one)
    videos[0].notes.append(new_note_for_video_1)
    db.session.commit()

    def teardown():
        all_notes = Note.query.all()
        for note_item in all_notes:
            db.session.delete(note_item)
            db.session.commit()


    request.addfinalizer(teardown)
    return {"video_with_notes": videos[0], "video_without_notes": videos[1], "note_data": note_fixture_one, "video_id":videos[0].id, "note_id": new_note_for_video_1.id  }


@pytest.fixture(scope="function")
def valid_user_has_watched_first_video(init_db, populate_db_with_valid_user, populate_db_with_videos_and_categories, request):
    db = init_db

    all_videos = populate_db_with_videos_and_categories["videos"]
    valid_user = populate_db_with_valid_user
    valid_user.watched_videos.append(all_videos[0])
    db.session.commit()
    return {"user":valid_user, "watched_video": all_videos[0], "all_videos":all_videos}


@pytest.fixture(scope="function")
def drop_all_users(test_client, init_db):
    User.query.delete()
    init_db.session.commit()
