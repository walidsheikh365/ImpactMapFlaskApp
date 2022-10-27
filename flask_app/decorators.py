from functools import wraps
from flask import flash, redirect, url_for
from flask_login import current_user


def check_confirmed(func):
    """Checks user verification status"""
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if current_user.verified is False:
            flash('Please confirm your account!', 'warning')
            return redirect(url_for('user.unconfirmed'))
        return func(*args, **kwargs)
    return decorated_function
