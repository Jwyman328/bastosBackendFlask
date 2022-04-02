from flask.cli import FlaskGroup
from dal.User_dal import UserDal
# all the imports
from manage import db
from models.Articles import Article
from models.Categories import Category
from models.Books import Book
from models.Videos import Video
from models.Notes import Note
from app import app
from fixtures.book_fixtures import fundamentos_de_la_libertad
from fixtures.video_fixtures import video_fixture, video_fixture_2
from fixtures.note_fixtures import note_fixture_one

cli = FlaskGroup(app)


@cli.command("seed_db")
def seed_db():
    UserDal.create_new_user(password="password1",
                            username="michael@mherman.org")

    horror = Category(category="Horror")
    economics = Category(category="economics")
    history = Category(category="history")
    allType = Category(category="allType")
    allInstitute = Category(category="allInstitute") 
    article_1 = Article(url="www.myurl.com", imageUrl="www.myimageurl.com",
                        title="the best article", date="2014-02-10")

    article_2 = Article(url="www.myurl.com", imageUrl="www.myimageurl.com",
                        title="the best article",date="2014-02-11" )

    fundamentos_de_la_libertad_instance = Book(**fundamentos_de_la_libertad)
    fundamentos_de_la_libertad_instance.catagories.append(economics)

    ## seed db with videos and notes
    video_1 = Video(title=video_fixture["title"], image=video_fixture["image"], noteCount=video_fixture["noteCount"], year=video_fixture["year"], videoUrl=video_fixture["videoUrl"])
    video_2 = Video(title=video_fixture_2["title"], image=video_fixture_2["image"], noteCount=video_fixture_2["noteCount"], year=video_fixture_2["year"], videoUrl=video_fixture_2["videoUrl"])
    video_1.categories.extend([horror, economics, allType, allInstitute])
    video_2.categories.extend([history, allType, allInstitute])
    new_note_for_video_1 = Note(noteText=note_fixture_one["noteText"], noteTitle=note_fixture_one["noteTitle"], videoTimeNoteTakenInSeconds=note_fixture_one["videoTimeNoteTakenInSeconds"])
    video_1.notes.append(new_note_for_video_1)

    db.session.add_all([article_2, article_1, horror, history,  economics, fundamentos_de_la_libertad_instance, video_1, video_2 ])
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
