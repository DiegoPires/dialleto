from app import db
from .BaseMixin import BaseMixin

class Language(BaseMixin, db.Model):

    name = db.Column(db.String(60), unique=True, nullable=False)
    code = db.Column(db.String(6), unique=True, nullable=False)

    color = db.Column(db.String(7))

    parent_id = db.column(db.Integer, db.ForeignKey('languages.id'))

    texts = db.relationship('Text', backref='language_texts', lazy='dynamic')
    tags  = db.relationship('Tag', backref='language_tag', lazy='dynamic')
    #sons = db.relationship('Language', backref='language_sons', lazy='dynamic')

    #sons = db.relationship('Language',
    #                       backref=db.backref('language_sons', remote_side='Language.id'),
     #                      viewonly=True,
    #                       lazy='dynamic')
    def __repr__(self):
        return '<Language: {}>'.format(self.name)
