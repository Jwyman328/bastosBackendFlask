from models.Articles import Article


class ArticleDal():

    @staticmethod
    def get_all_articles():
        all_articles = Article.query.all()
        json_articles = []
        for article_item in all_articles:
            json_articles.append(
                article_item.get_articles_and_related_categories_as_jsonable())

        return json_articles
