from flask.cli import FlaskGroup
from dal.User_dal import UserDal
# all the imports
from manage import db
from models.Articles import Article
from models.Categories import Category
from models.Books import Book
from app import app
from fixtures.book_fixtures import fundamentos_de_la_libertad
cli = FlaskGroup(app)


@cli.command("seed_db")
def seed_db():
    UserDal.create_new_user(password="password1",
                            username="michael@mherman.org")

    horror = Category(category="Horror")
    economics = Category(category="economics")
    history = Category(category="history")

    article_1 = Article(url="www.myurl.com", imageUrl="www.myimageurl.com",
                        title="the best article")

    article_2 = Article(url="www.myurl.com", imageUrl="www.myimageurl.com",
                        title="the best article", )

    fundamentos_de_la_libertad_instance = Book(**fundamentos_de_la_libertad)
    fundamentos_de_la_libertad_instance.catagories.append(economics)
    db.session.add_all([article_2, article_1, horror, history,  economics, fundamentos_de_la_libertad_instance])
    db.session.commit()
    article_1.categories.append(horror)
    db.session.commit()


@cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


if __name__ == "__main__":
    cli()
