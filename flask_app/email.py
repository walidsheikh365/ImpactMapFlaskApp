from flask_app.app import mail
from flask_mail import Message
from flask_app.config import Config


def send_email(to, template):
    """Sends verification email"""
    msg = Message('Please confirm your email',
                  sender=Config.MAIL_DEFAULT_SENDER,
                  recipients=[to])
    msg.html = template
    mail.send(msg)
