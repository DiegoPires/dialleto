from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager
from .BaseMixin import BaseMixin

class Lexicographer(UserMixin, BaseMixin,  db.Model):

    email = db.Column(db.String(60), index=True, unique=True)
    username = db.Column(db.String(60), index=True, unique=True)
    first_name = db.Column(db.String(60), index=True)
    last_name = db.Column(db.String(60), index=True)
    password_hash = db.Column(db.String(128))

    words = db.relationship('Word', backref='lexicographer', lazy='dynamic')
    ratings = db.relationship('Rating', backref='lexicographer', lazy='dynamic')
    languages = db.relationship('Language', backref='lexicographer', lazy='dynamic')
    texts = db.relationship('Text', backref='lexicographer', lazy='dynamic')
    words = db.relationship('Word', backref='lexicographer', lazy='dynamic')

    @property
    def password(self):
        # Prevent password from being accessed
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        # Set password to a hashed password
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        # Check if hashed password matches actual password
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<Lexicographer: {}>'.format(self.username)

    # Set up user_loader
    @login_manager.user_loader
    def load_user(user_id):
        return Lexicographer.query.get(int(user_id))