import pytest
import sqlite3
from project import db
from project import create_app
from project.models import User, Ttable, Task

@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app('TEST')

    testing_client = flask_app.test_client()

    ctx = flask_app.app_context()
    ctx.push()

    yield testing_client

    ctx.pop()

@pytest.fixture(scope='module')
def init_database():
    # Create the database and the database table
    db.create_all()

    # Insert user data
    user1 = User(email='joedoe@example.com', password='sha256$LyT5tEgF$0c2395bbb18494ad59b6a425c701e4d7c477d17ae8fdf90cd9cb29aa29867944', name='Joe')
    user2 = User(email='mikedoe@example.com', password='PaSsWoRd', name='Mike')
    db.session.add(user1)
    db.session.add(user2)

    # Commit the changes for the users
    db.session.commit()

    yield db  # this is where the testing happens!

    db.drop_all()

