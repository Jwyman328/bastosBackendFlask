import pytest
from models.Videos import Video
from models.Categories import Category
from fixtures.video_fixtures import video_fixture
from fixtures.category_fixtures import category_horror_fixture

def test_video_is_made_and_category_links_with_backref(test_client):
    first_video = Video(**video_fixture)
    horror_category = Category(category = category_horror_fixture)
    first_video.categories.append(horror_category)
    assert len(first_video.categories) == 1

    # category back ref refs the Video
    assert len(horror_category.videos) == 1


def test_get_video_and_related_categories_as_jsonable(test_client):
    first_video = Video(**video_fixture)
    horror_category = Category(category = category_horror_fixture)
    first_video.categories.append(horror_category)

    # as array of categories
    video_fixture["categories"] = [category_horror_fixture]
    assert first_video.get_video_and_related_categories_as_jsonable() == video_fixture
