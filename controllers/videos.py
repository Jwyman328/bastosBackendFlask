from models.Videos import Video
from dal.Videos_dal import VideoDal
from flask import Blueprint, jsonify, request, Response
from flask_jwt_extended import jwt_required
from controllers.helpers.auth_helpers import get_current_user_by_jwt

videos_controller = Blueprint("videos", __name__)

@videos_controller.route("/videos/")
@jwt_required()
def get_all_videos():
    ## eventuall add if it has been watched
    current_user = get_current_user_by_jwt()
    user_id = current_user.id
    all_videos = VideoDal.get_all_videos(user_id)
    return jsonify(all_videos)

@videos_controller.route("/videos/", methods=["POST"])
@jwt_required()
def mark_video_as_watched():
    current_user = get_current_user_by_jwt()
    user_id = current_user.id
    video_id = request.json['videoID']

    watched_video = VideoDal.mark_video_as_watched(user_id, video_id)

    return Response( status=201, mimetype='application/json')
