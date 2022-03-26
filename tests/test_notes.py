from models.Notes import Note
from models.Videos import Video
from fixtures.note_fixtures import note_fixture_one
from fixtures.video_fixtures import video_fixture

def test_note_creation():
    video_for_notes = Video(**video_fixture)
    video_for_notes.id = 1
    new_note = Note(note_text=note_fixture_one["noteText"], note_title=note_fixture_one["noteTitle"], video_time_note_taken_in_seconds=note_fixture_one["videoTimeNoteTakenInSeconds"])

    assert new_note.video_time_note_taken_in_seconds == note_fixture_one["videoTimeNoteTakenInSeconds"]
    assert new_note.note_title == note_fixture_one["noteTitle"]
    assert new_note.note_text == note_fixture_one["noteText"]

