from app import db
from .BaseMixin import BaseMixin

class Definition(BaseMixin, db.Model):

    word_id = db.column(db.Integer, db.ForeignKey('words.id'))
    language_id = db.Column(db.Integer, db.ForeignKey('languages.id'))

    texts = db.relationship('Text', backref='definition', lazy='dynamic')
    ratings = db.relationship('Rating', backref='definition', lazy='dynamic')

    def __repr__(self):
        return '<Definition: {}>'.format(self.name)