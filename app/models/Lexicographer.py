from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager
from datetime import datetime

from .Word import Word

class Lexicographer(UserMixin, db.Model):
    # Create an Lexicographer table

    # Ensures table will be named in plural and not in singular
    # as is the name of the model
    __tablename__ = 'lexicographers'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), index=True, unique=True)
    username = db.Column(db.String(60), index=True, unique=True)
    first_name = db.Column(db.String(60), index=True)
    last_name = db.Column(db.String(60), index=True)
    password_hash = db.Column(db.String(128))

    words = db.relationship('Word', backref='lexicographer', lazy='dynamic')

    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

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