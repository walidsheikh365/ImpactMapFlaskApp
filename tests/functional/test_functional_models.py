import sys
from flask_app.auth.routes import delete_account, login
sys.path.append('.')
from flask_app.models import User
from flask_app import db

# The following doesn't use the new_user fixture as the test is used before that fixture is created in the activities
def test_user_table_has_one_more_row():
    """
        GIVEN the app is created with a database
        WHEN a new user is inserted in the User table
        THEN the row count should increase by one
    """
    user_data = {
        'first_name': 'Alice',
        'last_name': 'Cooper',
        'password_text': 'SchoolsOut',
        'email': 'a_cooper@poison.net'
    }

    row_count_start = User.query.count()
    new_user = User(first_name=user_data['first_name'], last_name=user_data['last_name'], email=user_data['email'],
                    password_text=user_data['password_text'], verified=False)
    db.session.add(new_user)
    db.session.commit()
    row_count_end = User.query.count()
    assert row_count_end - row_count_start == 1
