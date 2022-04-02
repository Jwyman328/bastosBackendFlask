from manage import db
from models.Base import Base

# TODO change noteTitle and noteText to snake case 
class Note(db.Model, Base):
    id = db.Column(db.Integer, primary_key=True)

    videoTimeNoteTakenInSeconds = db.Column(db.Float)
    noteTitle = db.Column(db.String)
    noteText = db.Column(db.String)
    video_id = db.Column(db.Integer, db.ForeignKey('video.id'), nullable=False )
    

    def __init__(self, videoTimeNoteTakenInSeconds, noteTitle, noteText):
        self.videoTimeNoteTakenInSeconds = videoTimeNoteTakenInSeconds
        self.noteTitle = noteTitle 
        self.noteText = noteText 

    def get_note_as_json_with_video_backref_jsoned(self):
        json_note = self.__json__()
        return json_note
