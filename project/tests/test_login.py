import pytest
import sqlite3
from project import db
from project import create_app
from project.models import User, Ttable, Task

@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app()

    testing_client = flask_app.test_client()

    ctx = flask_app.app_context()
    ctx.push()

    yield testing_client

    ctx.pop()

@pytest.fixture
def init_database():
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()
    cursor.execute('''
      CREATE TABLE user
        (email, password, name)''')
    sample_data = [
        ('johndoe@example.com', 'admin', 'John'),
        ('mikedoe@example.com', 'admin', 'Mike'),
    ]
    cursor.executemany('INSERT INTO user VALUES(?, ?, ?)', sample_data)
    yield conn


def test_connection(init_database):
    """
    GIVEN a database
    WHEN two users are inserted
    THEN check if there are 2 records in the database
    """
    cursor = init_database
    assert len(list(cursor.execute('SELECT * FROM user'))) == 2

def test_login_page(test_client):
    """
    GIVEN a Flask application
    WHEN the '/' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get('/login')
    assert response.status_code == 200
    assert b"Login" in response.data
    assert b"Remember me" in response.data

def test_valid_login_logout(test_client, init_database):
    """
    GIVEN a Flask application
    WHEN the '/login' page is posted to (POST)
    THEN check the response is valid
    """
    response = test_client.post('/login',
                                data=dict(email='johndoe@example.com', password='admin'),
                                follow_redirects=True)
    assert response.status_code == 200

    """
    GIVEN a Flask application
    WHEN the '/logout' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
    assert b"Logout" not in response.data
    assert b"Login" in response.data
