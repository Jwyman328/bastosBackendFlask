from manage import db


video_category = db.Table("video_category",
                            db.Column("video_id", db.Integer,
                                      db.ForeignKey("video.id")),
                            db.Column("category_id", db.Integer,
                                      db.ForeignKey("category.id"))
                            )
