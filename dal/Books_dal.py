
from models.Books import Book
from models.Users import User 
from manage import db
class BookDal():

    @staticmethod
    def get_all_books_from_db(user_id):
        json_books = []
        all_books = Book.query.join(Book.catagories).all()
        for book in all_books:
            hasBeenReadByUser = book.has_been_read_by_user(user_id)
            book_as_json = book.get_books_and_related_categories_as_jsonable()
            book_as_json["hasBeenReadByUser"] = hasBeenReadByUser
            book_as_json["_id"] = book.id
            ## remove user objects
            delattr(book, "read_by_users")

            json_books.append(book_as_json)
        return json_books

    @staticmethod
    def mark_book_as_read(user_id, book_id):
        book_to_be_marked_as_read = Book.query.filter_by(id=book_id).first()
        user = User.query.filter_by(id=user_id).first()
        user.read_books.append(book_to_be_marked_as_read)
        db.session.commit()

    @staticmethod
    def mark_book_as_unread(user_id, book_id):
        user = User.query.filter_by(id=user_id).first()

        new_read_books = list(filter(lambda book: book.id != int(book_id), user.read_books))

        user.read_books = new_read_books
        db.session.commit()


        