from flask import Blueprint, render_template, flash, redirect, url_for, request, abort
from sqlalchemy.exc import IntegrityError
from urllib.parse import urlparse, urljoin
from datetime import timedelta, datetime
from flask_app import db, login_manager
from flask_app.auth.forms import SignupForm, LoginForm, DeleteUserForm, PasswordForm
from flask_app.decorators import check_confirmed
from flask_app.models import User
from flask_login import login_user, logout_user, login_required, current_user


auth_bp = Blueprint('auth', __name__)


@login_manager.user_loader
def load_user(user_id):
    """Takes a user ID and returns a user object or None if user doesnt exist"""
    if user_id is not None:
        return User.query.get(user_id)
    return None

@login_manager.unauthorized_handler
def unauthorized():
    """Redirect unauthorized users to Login page."""
    flash('You must be logged in to view that page.')
    return redirect(url_for('auth.login'))


def is_safe_url(target):
    host_url = urlparse(request.host_url)
    redirect_url = urlparse(urljoin(request.host_url, target))
    return redirect_url.scheme in ('http', 'https') and host_url.netloc == redirect_url.netloc

def get_safe_redirect():
    url = request.args.get('next')
    if url and is_safe_url(url):
        return url
    url = request.referrer
    if url and is_safe_url(url):
        return url
    return '/'


@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    from flask_app.email import send_email
    from flask_app.token import generate_verification_token

    signup_form = SignupForm(request.form)
    if signup_form.validate_on_submit():
        user = User(signup_form.first_name.data, signup_form.last_name.data, signup_form.email.data, signup_form.password.data, verified=False)
        try:
            db.session.add(user)
            db.session.commit()
            # Generate verification email
            token = generate_verification_token(user.email)
            confirm_url = url_for('auth.verify_email', token=token, _external=True)
            html = render_template('verify.html', confirm_url=confirm_url)
            send_email(user.email, html)

            login_user(user)
            flash('A verification email has been sent via email.', 'success')    
        except IntegrityError as err:
            db.session.rollback()
            flash(f'Error, unable to register {signup_form.email.data}.', 'error ')
            print(err)
            return redirect(url_for('auth.signup'))
        return redirect(url_for('auth.unconfirmed'))
    return render_template('signup.html', title='Sign Up', form=signup_form)


@auth_bp.route('/verify/<token>')
def verify_email(token):
    """Verifies if the token sent is equal to the token received"""
    from flask_app.token import verify_token

    try:
        email = verify_token(token)
    except:
        flash('The verification link is invalid or has expired.', 'danger')
    user = User.query.filter_by(email=email).first_or_404()
    if user.verified:
        flash('Account already verified. Please login.', 'success')
    else:
        user.verified = True
        user.verified_on = datetime.now()
        db.session.add(user)
        db.session.commit()
        flash('You have verified your account. Thanks!', 'success')
    return redirect(url_for('main.index'))


@auth_bp.route('/unconfirmed')
@login_required
def unconfirmed():
    """Generates a page asking for account verification"""
    if current_user.verified:
        return redirect('main.index')
    flash('Please verify your account!', 'warning')
    return render_template('unconfirmed.html')


@auth_bp.route('/resend')
@login_required
def resend_verification():
    """Generates a different page when resending the verification email"""
    from flask_app.email import send_email
    from flask_app.token import generate_verification_token

    token = generate_verification_token(current_user.email)
    confirm_url = url_for('auth.verify_email', token=token, _external=True)
    html = render_template('verify.html', confirm_url=confirm_url)
    send_email(current_user.email, html)
    flash('A new verification email has been sent.', 'success')
    return redirect(url_for('auth.unconfirmed'))


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = User.query.filter_by(email=login_form.email.data).first()
        if login_form.remember_me.data:
            login_user(user, remember=True, duration=timedelta(days=1))
        else:
            login_user(user)    # remember=False by default
        flash('Login successful.', 'success')
        next = request.args.get('next')
        if not is_safe_url(next):
            return abort(400)
        return redirect(next or url_for('main.index'))
    return render_template('login.html', title='Login', form=login_form)


@auth_bp.route('/profile/<id>', methods=['GET', 'POST'])
@login_required
@check_confirmed
def profile(id):
    """Gets profile page for a given user (password changes not working)"""
    password_form = PasswordForm()
    user = User.query.filter_by(id=id).first_or_404()
    if password_form.validate_on_submit():
        new_password = password_form.new_password.data
        user.set_password(new_password)
        flash('Password change successful', 'success')
    return render_template('profile.html', title="Change Password", form=password_form, user=user)


@auth_bp.route('/logout')
@login_required
def logout():
    """Logs out user"""
    logout_user()
    flash(f'See you next time!')
    return redirect(url_for('main.index'))


@auth_bp.route('/delete_account/<id>', methods=['GET', 'POST'])
@login_required
def delete_account(id):
    """Deletes user account from database"""
    deletion_form = DeleteUserForm()
    if deletion_form.validate_on_submit():
        User.query.filter_by(id=id).delete()
        db.session.commit()
        flash('Account has been successfully deleted.', 'success')
        return redirect(url_for('main.index'))
    return render_template('delete_account.html', title='Delete Account', form=deletion_form)
