from flask_app import db
from flask_app.models import User


def setUp(self):
    """Additional use for testing"""
    db.create_all()
    user = User(email="ad@min.com", password="admin_user", verified=False)
    db.session.add(user)
    db.session.commit()