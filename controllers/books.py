from flask import Blueprint, jsonify, request, Response

from models.Books import Book
from dal.Books_dal import BookDal
from dal.User_dal import UserDal
from flask_jwt_extended import jwt_required, get_jwt
from controllers.helpers.auth_helpers import get_current_user_by_jwt

books_controller = Blueprint("books", __name__)

# the exta / is bad practice but currently what is done in the frontend
@books_controller.route("/books/")
@jwt_required()
def get_all_books():
    current_user = get_current_user_by_jwt()
    user_id = current_user.id
    all_books = BookDal.get_all_books_from_db(user_id)
    return jsonify(all_books)

@books_controller.route("/books/read/", methods=["POST"])
@jwt_required()
def mark_book_as_read():
    current_user = get_current_user_by_jwt()
    user_id = current_user.id
    book_id = request.json['bookId']

    BookDal.mark_book_as_read(user_id, book_id)

    return Response(status=201, mimetype='application/json')


@books_controller.route("/books/read/", methods=["DELETE"])
@jwt_required()
def remove_book_as_read():
    current_user = get_current_user_by_jwt()
    user_id = current_user.id
    book_id_to_be_deleted = request.args.get("id")
    BookDal.mark_book_as_unread(user_id, book_id_to_be_deleted)
    
    return Response( status=204, mimetype='application/json')

