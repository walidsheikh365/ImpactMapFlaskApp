import sys
sys.path.append('.')
from flask_app.models import User


def test_new_user_details_correct():
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the fields are defined correctly
    """
    user_data = {
        'first_name': 'Samwise',
        'last_name': 'Gamgee',
        'email': 'email@gmail.com',
        'password_text': 'wordpass'
    }

    user = User(
        first_name=user_data['first_name'],
        last_name=user_data['last_name'],
        email=user_data['email'],
        password_text=user_data['password_text'],
        verified=False
    )

    assert user.first_name == 'Samwise'
    assert user.last_name == 'Gamgee'
    assert user.email == 'email@gmail.com'
    assert user.password != 'wordpass'