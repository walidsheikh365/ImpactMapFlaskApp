import secrets
import pathlib
import os


class Config(object):
    # main config
    SECRET_KEY = secrets.token_urlsafe(16)
    SECURITY_PASSWORD_SALT = secrets.token_urlsafe(16)
    WTF_CSRF_SECRET_KEY = secrets.token_urlsafe(16)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    database_file = pathlib.Path(__file__).parent.joinpath("data", "flask_app.sqlite")
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + str(database_file)
    TESTING = False

    # mail settings
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True

    # gmail authentication
    MAIL_USERNAME = 'flaskaccoun@gmail.com'
    MAIL_PASSWORD = 'flask.accoun1'

    # mail accounts
    MAIL_DEFAULT_SENDER = 'flaskaccoun@gmail.com'


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    database_file = pathlib.Path(__file__).parent.parent.joinpath("data", "flask_app.sqlite")
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + str(database_file)
    SQLALCHEMY_ECHO = True


class TestingConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_ECHO = True

    # mail settings
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True

    # gmail authentication
    MAIL_USERNAME = 'flaskaccoun@gmail.com'
    MAIL_PASSWORD = 'flask.accoun1'

    # mail accounts
    MAIL_DEFAULT_SENDER = 'flaskaccoun@gmail.com'
