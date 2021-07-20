from project import create_app
from project.models import User

def test_home_page():
    """
    GIVEN a Flask application configured for testing
    WHEN the '/' page is called (GET)
    THEN check that a '200' status code is returned
    """
    flask_app = create_app()

    with flask_app.test_client() as test_client:
        response = test_client.get('/')
        assert response.status_code == 200

def test_login_page():
    """
    GIVEN a Flask application configured for testing
    WHEN the '/profile' page is called (GET)
    THEN check that a '200' status code is returned
    """
    flask_app = create_app()

    with flask_app.test_client() as test_client:
        response = test_client.get('/login')
        assert response.status_code == 200
