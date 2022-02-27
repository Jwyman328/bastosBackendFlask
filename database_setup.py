from flask.cli import FlaskGroup
# all the imports
from manage import app, db
from models.Users import User

cli = FlaskGroup(app)


@cli.command("seed_db")
def seed_db():
    db.session.add(User(email="michael@mherman.org", first_name="steve"))
    db.session.commit()


@cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


if __name__ == "__main__":
    cli()
