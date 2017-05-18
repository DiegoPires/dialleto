from app import db
from .BaseMixin import BaseMixin

class Language(BaseMixin, db.Model):

    name = db.Column(db.String(60), unique=True, nullable=False)
    code = db.Column(db.String(6), unique=True, nullable=False)

    parent_id = db.column(db.Integer, db.ForeignKey('languages.id'))

    definitions = db.relationship('Definition', backref='language', lazy='dynamic')
    sons = db.relationship('Language', backref='language', lazy='dynamic')

    def __repr__(self):
        return '<Language: {}>'.format(self.name)
