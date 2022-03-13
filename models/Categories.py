from manage import db


class Category(db.Model):
    # __tablename__ = "categories"
    id = db.Column(db.Integer, primary_key=True)

    category = db.Column(db.String)

    def __init__(self, category):
        self.category = category
