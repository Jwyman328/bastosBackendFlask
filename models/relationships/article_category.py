from manage import db


article_category = db.Table("article_category",
                            db.Column("article_id", db.Integer,
                                      db.ForeignKey("article.id")),
                            db.Column("category_id", db.Integer,
                                      db.ForeignKey("category.id"))
                            )
