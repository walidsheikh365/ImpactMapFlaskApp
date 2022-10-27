import sys
from flask_app.auth.routes import delete_account
sys.path.append('.')
from flask_app.models import User
from flask_app import db
from flask_login import login_user, logout_user


def login(client, email, password):
    """Provides login to be used in tests"""
    return client.post('/login', data=dict(
        email=email,
        password=password
    ), follow_redirects=True)

def logout(client):
    """Provides logout to be used in tests"""
    return client.get('/logout', follow_redirects=True)

def profile(client, id):
    """Provides access to user profile page"""
    return client.get(f'/profile/<{id}>', follow_redirects=True)


def test_user_login_success(new_user, test_client):
    """
    GIVEN a user with a valid username and password
    WHEN the user logs in
    THEN a HTTP 200 code is received
    """
    db.session.add(new_user)
    db.session.commit()
    response = login(test_client, new_user.email, new_user.password)
    assert response.status_code == 200

def test_signup_succeeds(test_client):
    """
    GIVEN A user is not registered
    WHEN they submit a valid registration form
    THEN they should be redirected to a page with a custom welcome message and there should be an
    additional record in the user table in the database
    """
    count = User.query.count()
    response = test_client.post('/signup', data=dict(
        first_name='Person',
        last_name='Two',
        email='person_2@people.com',
        password='password2',
        password_repeat='password2'
    ), follow_redirects=True)
    count2 = User.query.count()
    assert count2 - count == 1
    assert response.status_code == 200
    assert b'Person' in response.data

def test_login_email_not_found(new_user, test_client):
    """
    GIVEN a User has been created
    WHEN the user logs in with the wrong email address
    THEN then an error message should be displayed on the login form ('No account found with that email address.')
    """
    db.session.add(new_user)
    db.session.commit()
    response = login(test_client, 'incorrectemail@gmail.com', new_user.password)
    assert response.status_code == 200
    assert b'No account found with that email address.' in response.data

def test_login_password_not_found(new_user, test_client):
    """
    GIVEN a User has been created
    WHEN the user logs in with the wrong password
    THEN then an error message should be displayed on the login form ('Incorrect password.')
    """
    db.session.add(new_user)
    db.session.commit()
    response = login(test_client, new_user.email, 'incorrectpassword')
    assert response.status_code == 200
    assert b'Incorrect password.' in response.data

def test_login_option_in_navbar(new_user, test_client):
    """
    GIVEN a User logged out
    WHEN they access the navigation bar
    THEN there should be an option to login in
    """
    db.session.add(new_user)
    db.session.commit()
    response = login(test_client, new_user.email, new_user.password)
    assert b'Logout' in response.data
    logout(test_client)
    assert response.status_code == 200
    assert b'Login' in response.data

def test_profile_redirect_if_not_logged_in(new_user, test_client):
    """
    GIVEN A user is registered but not logged in
    WHEN they attempt to access the profile page
    THEN they should be redirected to the login page
    """
    db.session.add(new_user)
    db.session.commit()
    response = profile(test_client, new_user.id)
    assert b'You must be logged in to view that page.' in response.data
