from project import create_app
from project.models import User, Ttable, Task

def test_user_model():
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

def test_ttable_model():
    """
    GIVEN a Ttable model
    WHEN a new Ttable is created
    THEN check email and name fields are defined correctly
    """
    flask_app = create_app()

    with flask_app.test_client() as test_clinet:
        ttable = Ttable(email='joedoe@example.com', name='Joe')
        assert ttable.email == 'joedoe@example.com'
        assert ttable.name == 'Joe'

def test_task_model():
    """
    GIVEN a Task model
    WHEN a new Task is created
    THEN check name, description and status fields are defined correctly
    """
    flask_app = create_app()

    with flask_app.test_client() as test_client:
        task = Task(name='Test', description='some random stuff', status=1)
        assert task.name == 'Test'
        assert task.description =='some random stuff'
        assert task.status == 1

