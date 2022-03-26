from manage import db
from models.Base import Base

# TODO change noteTitle and noteText to snake case 
class Note(db.Model, Base):
    id = db.Column(db.Integer, primary_key=True)

    video_time_note_taken_in_seconds = db.Column(db.Float)
    note_title = db.Column(db.String)
    note_text = db.Column(db.String)
    video_id = db.Column(db.Integer, db.ForeignKey('video.id'), nullable=False )
    

    def __init__(self, video_time_note_taken_in_seconds, note_title, note_text):
        self.video_time_note_taken_in_seconds = video_time_note_taken_in_seconds
        self.note_title = note_title 
        self.note_text = note_text 

    def get_note_as_json_with_video_backref_jsoned(self):
        json_note = self.__json__()
        return json_note
