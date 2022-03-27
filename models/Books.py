from manage import db
from models.Base import Base
from models.relationships.book_category import book_category

# I guess Category has to be imported because it is references in the categories relationship.
# https://stackoverflow.com/questions/61782453/flask-sqlalchemy-relationship-errors
from models.Categories import Category

class Book(db.Model, Base):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    image = db.Column(db.String)
    catagories = db.relationship(
        "Category", secondary=book_category, backref="book", lazy=False)
    author = db.Column(db.String)
    locationLink = db.Column(db.String)
    year = db.Column(db.Integer)

    def __init__(self, title, author, locationLink,
               year, image):
        self.title = title
        self.author = author
        self.locationLink = locationLink
        self.year = year
        self.image = image

    def get_json_categories_without_book_backref(self):
        json_categories = []
        for category_item in self.catagories:
            json_categories.append({"category": category_item.category})
        return json_categories

    def get_books_and_related_categories_as_jsonable(self):
        json_book = self.__json__()
        json_categories = self.get_json_categories_without_book_backref()
        json_book["catagories"] = json_categories
        return json_book

    def has_been_read_by_user(self, user_id):
        hasBeenReadByUser = False
        for user in self.read_by_users:
            if (user_id == user.id):
                hasBeenReadByUser = True
                break
            else:
                hasBeenReadByUser = False
        return hasBeenReadByUser
