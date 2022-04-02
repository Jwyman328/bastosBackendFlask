import json
from tests.helpers.helpers import create_authentication_header
from fixtures.note_fixtures import note_fixture_two

def test_get_notes_for_video(test_client,populate_db_with_valid_user,  populate_db_with_videos_and_notes,):
    video_without_notes = populate_db_with_videos_and_notes["video_without_notes"]
    video_with_notes =  populate_db_with_videos_and_notes["video_with_notes"]
    note = populate_db_with_videos_and_notes["note_data"]
    video_url = populate_db_with_videos_and_notes["video_url"]

    valid_user_session_token = populate_db_with_valid_user.session_token
    valid_user_request_headers = create_authentication_header(valid_user_session_token)
    
    response = test_client.get(f'/notes/{video_url}', headers=valid_user_request_headers)
    # convert json data to python
    response_data_as_python_dict = json.loads(response.get_data(as_text=True))
    assert len(response_data_as_python_dict) == 1

    assert note["videoTimeNoteTakenInSeconds"] == response_data_as_python_dict[0]["videoTimeNoteTakenInSeconds"]
    assert note["noteTitle"] == response_data_as_python_dict[0]["noteTitle"]
    assert note["noteText"] == response_data_as_python_dict[0]["noteText"]

def test_note_creation_through_post(test_client,populate_db_with_valid_user,  populate_db_with_videos_and_notes,):
    valid_user_session_token = populate_db_with_valid_user.session_token
    valid_user_request_headers = create_authentication_header(valid_user_session_token)
    video_without_notes = populate_db_with_videos_and_notes["video_without_notes"]
    
    note_data = {"videoId":video_without_notes.videoUrl, "noteTitle": note_fixture_two["noteTitle"], "noteText":note_fixture_two["noteText"], "videoTimeNoteTakenInSeconds": note_fixture_two["videoTimeNoteTakenInSeconds"]  }
    response = test_client.post("/notes/", headers=valid_user_request_headers, data=json.dumps(note_data))
    # convert json data to python
    # response_data_as_python_dict = json.loads(response.get_data(as_text=True))

    assert response.status == "201 CREATED"

    ## now you should be able to get the recently created note based off video id
    response = test_client.get(f'/notes/{video_without_notes.videoUrl}', headers=valid_user_request_headers)
    # convert json data to python
    response_data_as_python_dict = json.loads(response.get_data(as_text=True))
    assert len(response_data_as_python_dict) == 1
    assert response_data_as_python_dict[0]["noteTitle"] == note_data["noteTitle"]
    

def test_note_delete( test_client, populate_db_with_valid_user,  populate_db_with_videos_and_notes):
    valid_user_session_token = populate_db_with_valid_user.session_token
    valid_user_request_headers = create_authentication_header(valid_user_session_token)
    video_with_notes = populate_db_with_videos_and_notes["video_with_notes"]
    note_id = populate_db_with_videos_and_notes["note_id"]
    video_url = populate_db_with_videos_and_notes["video_url"]


    response = test_client.delete(f'/notes/{note_id}', headers=valid_user_request_headers)

    assert response.status == "200 OK"

    # now no notes should be returned for this video
    response = test_client.get(f'/notes/{video_url}', headers=valid_user_request_headers)
    # convert json data to python
    response_data_as_python_dict = json.loads(response.get_data(as_text=True))
    assert len(response_data_as_python_dict) == 0
    

def test_note_update(test_client, populate_db_with_valid_user,  populate_db_with_videos_and_notes):
    valid_user_session_token = populate_db_with_valid_user.session_token
    valid_user_request_headers = create_authentication_header(valid_user_session_token)
    video_with_notes = populate_db_with_videos_and_notes["video_with_notes"]
    note_id = populate_db_with_videos_and_notes["note_id"]
    
    updated_note_data = {"noteTitle": note_fixture_two["noteTitle"], "noteText":note_fixture_two["noteText"], "videoTimeNoteTakenInSeconds": note_fixture_two["videoTimeNoteTakenInSeconds"]  }

    response = test_client.put(f'/notes/{note_id}', headers=valid_user_request_headers, data=json.dumps(updated_note_data))

    assert response.status == "204 NO CONTENT"

    # now the note for this video should be the updated note 
    response = test_client.get(f'/notes/{video_with_notes.videoUrl}', headers=valid_user_request_headers)
    # convert json data to python
    response_data_as_python_dict = json.loads(response.get_data(as_text=True))
    assert len(response_data_as_python_dict) == 1

    assert updated_note_data["noteTitle"] == response_data_as_python_dict[0]["noteTitle"]
    assert updated_note_data["noteText"] == response_data_as_python_dict[0]["noteText"]

