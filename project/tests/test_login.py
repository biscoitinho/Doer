import pytest
import sqlite3
from project import db
from project import create_app
from project.models import User, Ttable, Task
from .fixtures import test_client, init_database

def test_profile_page_with_redirects(test_client):
    """
    GIVEN a Flask application
    WHEN the '/profile' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get('/profile', follow_redirects=True)
    assert b"Login" in response.data

def test_profile_page(test_client):
    """
    GIVEN a Flask application
    WHEN the '/profile' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get('/profile')
    assert response.status_code != 200

def test_login_page(test_client):
    """
    GIVEN a Flask application
    WHEN the '/login' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get('/login')
    assert response.status_code == 200
    assert b"Login" in response.data
    assert b"Remember me" in response.data

def test_login_unregistered_user(test_client, init_database):
    """
    GIVEN a Flask application
    WHEN the '/login' page is posted to (POST)
    THEN check the response is valid
    """
    response = test_client.post('/login',
                                data=dict(email='doe@example.com', password='123456'),
                                follow_redirects=True)
    assert response.status_code == 200
    assert b"Login" in response.data

def test_login(test_client, init_database):
    """
    GIVEN a Flask application
    WHEN the '/login' page is posted to (POST)
    THEN check the response is valid
    """
    response = test_client.post('/login',
                                data=dict(email='joedoe@example.com', password='admin'),
                                follow_redirects=True)
    assert response.status_code == 200
    assert b"Login" not in response.data
    assert b"Profile" in response.data

def test_profile_page_after_login(test_client, init_database):
    """
    GIVEN a Flask application
    WHEN the '/profile' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get('/profile', follow_redirects=True)
    assert response.status_code == 200

def test_logout(test_client, init_database):
    """
    GIVEN a Flask application
    WHEN the '/logout' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
    assert b"Logout" not in response.data
    assert b"Login" in response.data
