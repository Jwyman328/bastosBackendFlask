from flask.cli import FlaskGroup
from dal.User_dal import UserDal
# all the imports
from manage import db
from models.Users import User
from app import app

cli = FlaskGroup(app)


@cli.command("seed_db")
def seed_db():
    UserDal.create_new_user(password="password1",
                            username="michael@mherman.org")


@cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


if __name__ == "__main__":
    cli()
