from manage import db


user_watched_videos = db.Table("user_watched_videos",
                           db.Column("video_id", db.Integer,
                                     db.ForeignKey("video.id")),
                           db.Column("user_id", db.Integer,
                                     db.ForeignKey("users.id"))
                           )
