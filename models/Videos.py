from manage import db
from models.Base import Base
from models.relationships.video_category import video_category

class Video(db.Model, Base):

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String)
    image = db.Column(db.String)
    videoUrl = db.Column(db.String)
    noteCount = db.Column(db.Integer, default = 0)
    year = db.Column(db.Integer)

    categories = db.relationship(
        "Category", secondary=video_category, backref="videos", lazy=False)
    notes = db.relationship('Note', backref='video', lazy=True, cascade="all, delete")


    def __init__(self, title, image, videoUrl, noteCount, year):
        self.title = title 
        self.image = image 
        self.videoUrl = videoUrl 
        self.noteCount = noteCount 
        self.year = year
         

    def get_json_categories_without_book_backref(self):
        json_categories = []
        for category_item in self.categories:
            json_categories.append({"category": category_item.category})
        return json_categories

    def get_video_and_related_categories_as_jsonable(self):
        json_video = self.__json__()
        json_categories = self.get_json_categories_without_book_backref()
        json_video["categories"] = json_categories
        return json_video

    def has_been_watched_by_user(self, userId):
        hasBeenWatchedByUser = False
        for user in self.users_that_have_watched_this_video:
            if user.id == userId:
                hasBeenWatchedByUser = True
                break
        return hasBeenWatchedByUser

