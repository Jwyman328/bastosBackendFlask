
from models.Articles import Article
from models.Categories import Category
from fixtures.article_fixtures import article_1_fixture, article_2_fixture
from fixtures.category_fixtures import category_economics_fixture, category_history_fixture


def test_articles(test_client, init_db, populate_db_with_articles_and_categories):
    # test first two articles are generated with the corresponding categories and
    # you can reference them from articles and categories
    article_2 = Article.query.filter_by(url=article_2_fixture["url"]).first()
    article_1 = Article.query.filter_by(url=article_1_fixture["url"]).first()
    history_category = Category.query.filter_by(
        category=category_history_fixture).first()
    economics_category = Category.query.filter_by(
        category=category_economics_fixture).first()

    assert len(article_1.categories) == 2
    assert len(article_2.categories) == 3
    assert len(history_category.article) == 1
    assert len(economics_category.article) == 2
