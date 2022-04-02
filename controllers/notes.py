from models.Videos import Video
from models.Notes import Note
from flask import Blueprint, jsonify, request, Response
from flask_jwt_extended import jwt_required
from controllers.helpers.auth_helpers import get_current_user_by_jwt
from dal.Notes_Dal import NotesDal

notes_controller = Blueprint("notes", __name__)

@notes_controller.route("/notes/<video_id>")
@jwt_required()
def get_all_notes(video_id):
    ## eventuall add if it has been watched
    current_user = get_current_user_by_jwt()
    all_notes = NotesDal.get_all_notes_for_video(video_id)
    return jsonify(all_notes)


@notes_controller.route("/notes/", methods=["POST"])
@jwt_required()
def create_note():
    current_user = get_current_user_by_jwt()
    user_id = current_user.id
    note_data_seconds = request.json['videoTimeNoteTakenInSeconds']
    note_data_videoID = request.json['videoId']
    note_data_title = request.json['noteTitle']
    note_data_text = request.json['noteText']

    new_note = NotesDal.create_note(user_id, note_data_videoID, note_data_seconds,note_data_title, note_data_text )
    # watched_video = VideoDal.mark_video_as_watched(user_id, video_id)

    return Response( status=201, mimetype='application/json')

@notes_controller.route("/notes/<note_id>", methods=["DELETE"])
@jwt_required()
def delete_note(note_id):
    # maybe make it so only the owner of the note can delete it.
    NotesDal.delete_note(note_id)

    return Response( status=200, mimetype='application/json')

@notes_controller.route("/notes/<note_id>", methods=["PUT"])
@jwt_required()
def update_note(note_id):
    # maybe make it so only the owner of the note can delete it.
    noteTitle = request.json['noteTitle']
    noteText = request.json['noteText']

    NotesDal.update_note(note_id, noteTitle, noteText)

    return Response( status=204, mimetype='application/json')

