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

def test_signup_page(test_client):
    """
    GIVEN a Flask application
    WHEN the '/login' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get('/signup')
    assert response.status_code == 200
    assert b"Sign Up" in response.data

def test_signup_login_logout(test_client, init_database):
    """
    GIVEN a Flask application
    WHEN the '/signup' page is posted to (POST)
    THEN check the response is valid
    """
    response = test_client.post('/signup',
                                data=dict(email='johndoe@example.com', name='John', password='admin123'),
                                follow_redirects=True)
    assert response.status_code == 200
    assert b"Login" in response.data

    """
    GIVEN a Flask application
    WHEN the '/login' page is posted to (POST)
    THEN check the response is valid
    """
    response = test_client.post('/login',
                                data=dict(email='johndoe@example.com', password='admin123'),
                                follow_redirects=True)
    assert response.status_code == 200
    assert b"Login" not in response.data
    assert b"Profile" in response.data

    """
    GIVEN a Flask application
    WHEN the '/profile' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get('/profile', follow_redirects=True)
    assert response.status_code == 200
    assert b"Welcome, John" in response.data

    """
    GIVEN a Flask application
    WHEN the '/logout' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
    assert b"Logout" not in response.data
    assert b"Login" in response.data
