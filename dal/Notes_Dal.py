from models.Videos import Video
from models.Notes import Note 
from manage import db

class NotesDal():

    @staticmethod
    def get_all_notes_for_video(video_id):
        video = Video.query.filter_by(id=video_id).first()
        all_notes = video.notes
        print("in dal all notes", all_notes)
        ## return jsonable array 
        jsonable_notes = []
        for note_item in all_notes:
            json_note = note_item.get_note_as_json_with_video_backref_jsoned()
            jsonable_notes.append(json_note)
        return jsonable_notes

    @staticmethod
    def create_note(user_id, video_id, note_data_seconds, note_data_title, note_data_text):
        video = Video.query.filter_by(id=video_id).first()
        new_note = Note(video_time_note_taken_in_seconds=note_data_seconds, note_title=note_data_title, note_text=note_data_text)
        video.notes.append(new_note)
        db.session.commit()
        return new_note.get_note_as_json_with_video_backref_jsoned()
        

    @staticmethod
    def delete_note(note_id):
       note_to_be_deleted = Note.query.filter_by(id=note_id).delete()
       db.session.commit()
        
    def update_note(note_id, updated_title, updated_text):
        note_to_be_deleted = Note.query.filter_by(id=note_id).update({"note_title":updated_title, "note_text": updated_text})
        db.session.commit()