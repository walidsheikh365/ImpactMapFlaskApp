from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_app import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    verified = db.Column(db.Boolean, nullable=False, default=False)
    verified_on = db.Column(db.DateTime, nullable=True)
    posts = db.relationship("Post", backref=db.backref('user'))
    comments = db.relationship("Comment", backref=db.backref('user'))

    def __init__(self, first_name: str, last_name: str, email: str, password_text: str, verified: bool, verified_on=None):
        """
        Create a new User object using hashing the plain text password.
        """
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.registered_on = datetime.now()
        self.password = self._generate_password_hash(password_text)
        self.verified = verified
        self.verified_on = verified_on

    def __repr__(self):
        return f"{self.id} {self.first_name} {self.last_name} {self.email} {self.password}"

    @staticmethod
    def _generate_password_hash(password_plaintext):
        return generate_password_hash(password_plaintext)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


class Post(db.Model):
    """Future additions"""
    __tablename__ = "post"
    post_id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_title = db.Column(db.Text, nullable=False)
    post_text = db.Column(db.Text, nullable=False)
    comments = db.relationship("Comment", backref=db.backref('post'))

    def __repr__(self):
        return '<Post %r>' % self.post_text


class Comment(db.Model):
    __tablename__ = "comment"
    comment_id = db.Column(db.Integer, primary_key=True)
    commenter_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.post_id'), nullable=False)
    comment_text = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return '<Comment %r>' % self.comment_text