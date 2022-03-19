from manage import db


user_read_books = db.Table("user_read_books",
                           db.Column("book_id", db.Integer,
                                     db.ForeignKey("book.id")),
                           db.Column("user_id", db.Integer,
                                     db.ForeignKey("users.id"))
                           )
