import pytest
from project import create_app
from project.models import User

@pytest.fixture(scope='module')
def new_app():
    flask_app = create_app()
    return flask_app

def test_home_page(new_app):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/' page is called (GET)
    THEN check that a '200' status code is returned
    """

    with new_app.test_client() as test_client:
        response = test_client.get('/')
        assert response.status_code == 200

def test_login_page(new_app):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/profile' page is called (GET)
    THEN check that a '200' status code is returned
    """

    with new_app.test_client() as test_client:
        response = test_client.get('/login')
        assert response.status_code == 200

def test_profile_page(new_app):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/profile' page is called (GET)
    THEN check that a '200' status code is returned
    """

    with new_app.test_client() as test_client:
        response = test_client.get('/signup')
        assert response.status_code == 200
