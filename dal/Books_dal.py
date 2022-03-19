
from models.Books import Book


class BookDal():

    @staticmethod
    def get_all_books_from_db(user_id):
        json_books = []
        all_books = Book.query.join(Book.catagories).all()
        for book in all_books:
            hasUserReadBook = book.has_been_read_by_user(user_id)
            book_as_json = book.get_books_and_related_categories_as_jsonable()
            book_as_json["hasUserReadBook"] = hasUserReadBook
            ## remove user objects
            delattr(book, "read_by_users")

            json_books.append(book_as_json)
        return json_books
