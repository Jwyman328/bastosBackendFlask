import json

from tests.helpers.helpers import create_json_articles_array_from_initial_articles


def test_get_articles(test_client, populate_db_with_articles_and_categories):
    response = test_client.get("/articles")
    data = json.loads(response.get_data(as_text=True))

    assert data == create_json_articles_array_from_initial_articles(
        populate_db_with_articles_and_categories)
