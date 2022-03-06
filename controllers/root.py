from flask import Blueprint

root_blueprint = Blueprint("root", __name__)


@root_blueprint.get('/')
def main_fun():
    return "hello world"
