from manage import db
from .relationships.article_category import article_category


class Article(db.Model):
    # __tablename__ = "articles"
    id = db.Column(db.Integer, primary_key=True)

    url = db.Column(db.String)
    imageUrl = db.Column(db.String)
    title = db.Column(db.String)
    date = db.Column(db.Date)
    categories = db.relationship(
        "Category", secondary=article_category, backref="article", lazy=True)

    def __init__(self, url, imageUrl, title):
        self.url = url
        self.imageUrl = imageUrl
        self.title = title

    # author: db.Column(db.String, ForeignKey("authord"))
