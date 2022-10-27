from flask_wtf import FlaskForm, Form
from wtforms import StringField, PasswordField, EmailField, BooleanField, SubmitField
from wtforms.validators import DataRequired, EqualTo, ValidationError
from flask_app.models import User


class SignupForm(FlaskForm):
    first_name = StringField(label='First name', validators=[DataRequired()])
    last_name = StringField(label='Last name', validators=[DataRequired()])
    email = EmailField(label='Email address', validators=[DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    password_repeat = PasswordField(label='Repeat Password',
        validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    
    def validate_email(self, email):
        users = User.query.filter_by(email=email.data).first()
        if users is not None:
            raise ValidationError('An account is already registered for that email address')


class LoginForm(FlaskForm):
    email = EmailField(label='Email address', validators=[DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    remember_me = BooleanField(label='Remember me')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('No account found with that email address.')

    def validate_password(self, password):
        user = User.query.filter_by(email=self.email.data).first()
        if user is None:
            raise ValidationError('No account found with that email address.')
        if not user.check_password(password.data):
            raise ValidationError('Incorrect password.')


class DeleteUserForm(FlaskForm):
    delete_account = SubmitField('Delete user account')


class PasswordForm(FlaskForm):
    """Not working, available for future work"""
    current_password = StringField('Confirm Password', validators=[DataRequired()])
    new_password = StringField('New Password')

    """ def validate_password(self, current_password):
        user = User.query.filter_by(id=user.id).first()
        if not user.check_password(current_password.data):
            raise ValidationError('Incorrect password.') """