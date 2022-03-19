
def create_json_articles_array_from_initial_articles(initial_articles_and_categories):
    articles_and_categories = initial_articles_and_categories
    articles = articles_and_categories["articles"]
    json_article_data = []

    for item in articles:
        json_article_data.append(
            item.get_articles_and_related_categories_as_jsonable())

    return json_article_data


def create_authentication_header(user_token):
    return {"Content-Type": "application/json", "Authorization": f"Bearer {user_token}"}
