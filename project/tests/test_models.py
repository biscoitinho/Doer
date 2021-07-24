import pytest
from project import create_app
from project.models import User, Ttable, Task

@pytest.fixture(scope='module')
def new_user():
    user = User(email='joedoe@example.com', name='Mike', password='admin')
    return user

@pytest.fixture(scope='module')
def new_app():
    flask_app = create_app()
    return flask_app

def test_user_model(new_user, new_app):
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the email, hashed_password, and role fields are defined correctly
    """

    with new_app.test_client() as test_client:
        assert new_user.email == 'joedoe@example.com'
        assert new_user.password == 'admin'
        assert new_user.name == 'Mike'

def test_ttable_model(new_app):
    """
    GIVEN a Ttable model
    WHEN a new Ttable is created
    THEN check email and name fields are defined correctly
    """

    with new_app.test_client() as test_clinet:
        ttable = Ttable(email='joedoe@example.com', name='Joe')
        assert ttable.email == 'joedoe@example.com'
        assert ttable.name == 'Joe'

def test_task_model(new_app):
    """
    GIVEN a Task model
    WHEN a new Task is created
    THEN check name, description and status fields are defined correctly
    """

    with new_app.test_client() as test_client:
        task = Task(name='Test', description='some random stuff', status=1)
        assert task.name == 'Test'
        assert task.description =='some random stuff'
        assert task.status == 1

