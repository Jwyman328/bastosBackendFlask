from flask import Blueprint, jsonify

from dal.Articles_dal import ArticleDal

article_controller = Blueprint("articles", __name__)


@article_controller.route("/article")
def get_all_articles():
    all_articles = ArticleDal.get_all_articles()
    return jsonify(all_articles)
