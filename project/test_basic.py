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

def test_new_user():
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the email, hashed_password, and role fields are defined correctly
    """
    flask_app = create_app()

    with flask_app.test_client() as test_client:
        user = User(email='joedoe@example.com', name='Mike', password='admin')
        assert user.email == 'joedoe@example.com'
        assert user.password == 'admin'
        assert user.name == 'Mike'
