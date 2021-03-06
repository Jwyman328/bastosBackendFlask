from manage import db
from models.Base import Base
from .relationships.article_category import article_category

# I guess Category has to be imported because it is references in the categories relationship.
# https://stackoverflow.com/questions/61782453/flask-sqlalchemy-relationship-errors
from models.Categories import Category


class Article(db.Model, Base):
    # __tablename__ = "articles"
    id = db.Column(db.Integer, primary_key=True)

    url = db.Column(db.String)
    imageUrl = db.Column(db.String)
    title = db.Column(db.String)
    date = db.Column(db.String)
    categories = db.relationship(
        "Category", secondary=article_category, backref="article", lazy=True)

    def __init__(self, url, imageUrl, title, date):
        self.url = url
        self.imageUrl = imageUrl
        self.title = title
        self.date = date

    # author: db.Column(db.String, ForeignKey("authord"))

    def get_json_categories_without_article_backref(self):
        json_categories = []
        for category_item in self.categories:
            json_categories.append(category_item.category)
        return json_categories

    def get_articles_and_related_categories_as_jsonable(self):
        json_article = self.__json__()
        json_categories = self.get_json_categories_without_article_backref()
        json_article["categories"] = json_categories
        return json_article
