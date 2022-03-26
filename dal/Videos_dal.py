from models.Videos import Video
from models.Users import User
from manage import db

class VideoDal():

    @staticmethod
    def get_all_videos(user_id):
        ## only will return videos if it has a category
        ## TODO fix this
        all_videos = Video.query.join(Video.categories).all()
        all_videos_jsonable = []
        for video in all_videos:
            jsonable_video_data = video.get_video_and_related_categories_as_jsonable()
            jsonable_video_data["hasBeenWatchedByUser"] = video.has_been_watched_by_user(user_id)
            delattr(video, "users_that_have_watched_this_video")
            all_videos_jsonable.append(jsonable_video_data)
        
        return all_videos_jsonable 
    
    @staticmethod 
    def mark_video_as_watched(user_id, video_id):
        user = User.query.filter_by(id=user_id).first()

        watched_video = Video.query.filter_by(id=video_id).first()
        user.watched_videos.append(watched_video)
        db.session.commit()
        return watched_video

