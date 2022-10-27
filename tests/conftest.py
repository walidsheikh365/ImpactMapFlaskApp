import pytest
import sys
sys.path.append('.')
from flask_app import create_app, config
from flask_app.models import User


@pytest.fixture(scope='session')
def app():
    """Create a Flask app for the testing"""
    app = create_app(config_class_name=config.TestingConfig)
    yield app

@pytest.fixture(scope='session')
def test_client(app):
    """Create a Flask test client using the Flask app"""
    with app.test_client() as testing_client:
        # Establish an application context
        with app.app_context():
            yield testing_client

@pytest.fixture(scope='session')
def new_user():
    """Create a Flask test user"""
    new_user = User(first_name='James', last_name='Lee', email='james@gmail.com', password_text='james12345', verified=False)
    yield new_user