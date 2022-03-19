from manage import db


book_category = db.Table("book_category",
                         db.Column("book_id", db.Integer,
                                   db.ForeignKey("book.id")),
                         db.Column("category_id", db.Integer,
                                   db.ForeignKey("category.id"))
                         )
