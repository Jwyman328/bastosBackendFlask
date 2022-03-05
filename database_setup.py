from flask.cli import FlaskGroup
from dal.create_new_user import create_new_user
# all the imports
from manage import app, db
from models.Users import User

cli = FlaskGroup(app)


@cli.command("seed_db")
def seed_db():
    create_new_user(password="password1", username="michael@mherman.org")


@cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


if __name__ == "__main__":
    cli()
