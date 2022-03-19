from flask import Blueprint, jsonify

from models.Books import Book
from dal.Books_dal import BookDal
from dal.User_dal import UserDal
from flask_jwt_extended import jwt_required, get_jwt

books_controller = Blueprint("books", __name__)


@books_controller.route("/books")
@jwt_required()
def get_all_books():
    jwt = get_jwt()
    jti = jwt["jti"]
    current_user = UserDal.get_user_by_jti(jti)
    user_id = current_user.id
    all_books = BookDal.get_all_books_from_db(user_id)
    return jsonify(all_books)
