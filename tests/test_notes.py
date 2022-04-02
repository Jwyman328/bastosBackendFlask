from models.Notes import Note
from models.Videos import Video
from fixtures.note_fixtures import note_fixture_one
from fixtures.video_fixtures import video_fixture

def test_note_creation():
    video_for_notes = Video(**video_fixture)
    video_for_notes.id = 1
    new_note = Note(noteText=note_fixture_one["noteText"], noteTitle=note_fixture_one["noteTitle"], videoTimeNoteTakenInSeconds=note_fixture_one["videoTimeNoteTakenInSeconds"])

    assert new_note.videoTimeNoteTakenInSeconds == note_fixture_one["videoTimeNoteTakenInSeconds"]
    assert new_note.noteTitle == note_fixture_one["noteTitle"]
    assert new_note.noteText == note_fixture_one["noteText"]

