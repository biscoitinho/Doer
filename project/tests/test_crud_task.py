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

def test_create_task(test_client, init_database):
    """
    GIVEN a Flask application
    WHEN the '/tables/test_table/task/create' page is posted to (POST)
    THEN check the response is valid
    """
    response = test_client.post('/tables/test_table/task/create',
                                data=dict(name='test task', description='Do something', status='1'),
                                follow_redirects=True)
    assert response.status_code == 200

def check_create_task(test_client, init_database):
    """
    GIVEN a Flask application
    WHEN the '/tables/test_table/task/1' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get('/tables/test_table/task/1', follow_redirects=True)
    assert response.status_code == 200
    assert b"test task" in response.data

def test_edit_page(test_client, init_database):
    """
    GIVEN a Flask application
    WHEN the '/tables/test_table/task/1/edit' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get('/tables/test_table/task/1/edit', follow_redirects=True)
    assert response.status_code == 200

def test_edit_table(test_client, init_database):
    """
    GIVEN a Flask application
    WHEN the '/tables/test_table/task/1/edit' page is posted to (POST)
    THEN check the response is valid
    """
    response = test_client.post('/tables/test_table/task/1/edit',
                                data=dict(name='edit test task'),
                                follow_redirects=True)
    assert response.status_code == 200

def test_check_edit(test_client, init_database):
    """
    GIVEN a Flask application
    WHEN the '/tables/test_table/tasks' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get('/tables/test_table/tasks', follow_redirects=True)
    assert response.status_code == 200
    assert b"edit test task" in response.data

def test_delete_table(test_client, init_database):
    """
    GIVEN a Flask application
    WHEN the '/tables/test_table/task/1/delete' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get('/tables/test_table/task/1/delete', follow_redirects=True)
    assert response.status_code == 200

def test_check_delete_table(test_client, init_database):
    """
    GIVEN a Flask application
    WHEN the '/tables/test_table/tasks' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get('/tables/test_table/tasks', follow_redirects=True)
    assert response.status_code == 200
    assert b"edit test task" not in response.data

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
