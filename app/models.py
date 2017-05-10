from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager

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
    is_admin = db.Column(db.Boolean, default=False)

    words = db.relationship('Word', backref='lexicographer',
                                lazy='dynamic')

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

class Word(db.Model):
    # Create a Word table

    __tablename__ = 'words'

    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(60), unique=True)
    definition = db.Column(db.String(200))

    created_by_id = db.Column(db.Integer, db.ForeignKey('lexicographers.id'))
    language_id = db.Column(db.Integer, db.ForeignKey('languages.id'))

    def __repr__(self):
        return '<Word: {}>'.format(self.word)

class Language(db.Model):
    # Create a Language table

    __tablename__ = "languages"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    code = db.Column(db.String(6), unique=True)

    words = db.relationship('Word', backref='language',
                                lazy='dynamic')

    def __repr__(self):
        return '<Language: {}>'.format(self.name)
