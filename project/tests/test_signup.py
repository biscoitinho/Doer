import pytest
import sqlite3
from project import db
from project import create_app
from project.models import User, Ttable, Task
from .fixtures import test_client, init_database

def test_signup_page(test_client):
    """
    GIVEN a Flask application
    WHEN the '/login' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get('/signup')
    assert response.status_code == 200
    assert b"Sign Up" in response.data

def test_signup(test_client, init_database):
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

def test_login_with_new_user(test_client, init_database):
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

def test_profile_page_after_login(test_client, init_database):
    """
    GIVEN a Flask application
    WHEN the '/profile' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get('/profile', follow_redirects=True)
    assert response.status_code == 200
    assert b"Welcome, John" in response.data

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
