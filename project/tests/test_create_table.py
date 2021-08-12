import pytest
import sqlite3
from project import db
from project import create_app
from project.models import User, Ttable, Task
from .fixtures import test_client, init_database

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

def test_tables_page(test_client, init_database):
    """
    GIVEN a Flask application
    WHEN the '/tables' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get('/tables', follow_redirects=True)
    assert response.status_code == 200
    assert b"Create table" in response.data

def test_table_page(test_client, init_database):
    """
    GIVEN a Flask application
    WHEN the '/table' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get('/table', follow_redirects=True)
    assert response.status_code == 200
    assert b"Table" in response.data

def test_create_table(test_client, init_database):
    """
    GIVEN a Flask application
    WHEN the '/table' page is posted to (POST)
    THEN check the response is valid
    """
    response = test_client.post('/table',
                                data=dict(tablename='test table'),
                                follow_redirects=True)
    assert response.status_code == 200
    assert b"test table" in response.data
    assert b"Welcome, Joe here are your tables!" in response.data

def logout(test_client, init_database):
    """
    GIVEN a Flask application
    WHEN the '/logout' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
    assert b"Logout" not in response.data
    assert b"Login" in response.data
