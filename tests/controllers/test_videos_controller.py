from tests.helpers.helpers import create_authentication_header
import json 

def test_get_all_videos(test_client, populate_db_with_videos_and_categories, populate_db_with_valid_user):
    populated_video_1 = populate_db_with_videos_and_categories["videos"][0]
    populated_video_2 = populate_db_with_videos_and_categories["videos"][1]


    valid_user = populate_db_with_valid_user
    valid_user_request_headers = create_authentication_header(valid_user.session_token)

    response = test_client.get("/videos/", headers=valid_user_request_headers)
    response_data_as_python_dict = json.loads(response.get_data(as_text=True))

    jsonable_video_data_1 = populated_video_1.get_video_and_related_categories_as_jsonable()
    jsonable_video_data_1["hasBeenWatchedByUser"] = False
    jsonable_video_data_2 = populated_video_2.get_video_and_related_categories_as_jsonable()
    jsonable_video_data_2["hasBeenWatchedByUser"] = False

    assert response_data_as_python_dict == [jsonable_video_data_1, jsonable_video_data_2]


def test_get_all_videos_marked_as_watched_or_not(test_client, valid_user_has_watched_first_video):
    watched_video = valid_user_has_watched_first_video["watched_video"]

    valid_user = valid_user_has_watched_first_video["user"]
    valid_user_request_headers = create_authentication_header(valid_user.session_token)

    response = test_client.get("/videos/", headers=valid_user_request_headers)

    response_data_as_python_dict = json.loads(response.get_data(as_text=True))

    ## should return two videos and it should have watched_video hasBeenWatchedByUser set to true
    assert len(response_data_as_python_dict) == 2
    for video in response_data_as_python_dict:
        if video["id"] == watched_video.id:
            assert video["hasBeenWatchedByUser"] == True
        else:
            assert video["hasBeenWatchedByUser"] == False


def test_mark_video_as_watched(test_client, valid_user_has_watched_first_video):
    all_videos = valid_user_has_watched_first_video["all_videos"]
    unwatched_video = all_videos[1]

    valid_user = valid_user_has_watched_first_video["user"]
    assert unwatched_video.has_been_watched_by_user(valid_user.id) == False

    valid_user_request_headers = create_authentication_header(valid_user.session_token)
    video_data = {"videoID": unwatched_video.id }

    response = test_client.post("/videos/", headers=valid_user_request_headers, data=json.dumps(video_data))

    assert response.status == "201 CREATED"

    # get videos and now they all should be marked as watched 
    response = test_client.get("/videos/", headers=valid_user_request_headers)

    response_data_as_python_dict = json.loads(response.get_data(as_text=True))
    assert len(response_data_as_python_dict) == 2
    for video in response_data_as_python_dict:
        assert video["hasBeenWatchedByUser"] == True
