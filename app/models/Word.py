from app import db
from .BaseMixin import BaseMixin

class Word(BaseMixin, db.Model):

    word = db.Column(db.String(60), unique=True)

    definitions = db.relationship('Definition', backref='Word', lazy='dynamic')

    def __repr__(self):
        return '<Word: {}>'.format(self.word)