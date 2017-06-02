from app import db
from .BaseMixin import BaseMixin
from .TagText import TagText

import enum

class TextType(enum.Enum):
    Example = 1
    Definition = 2

class Text(BaseMixin, db.Model):

    text = db.Column(db.UnicodeText)
    type = db.Column(db.Enum(TextType))

    word_id = db.Column(db.Integer, db.ForeignKey('words.id'))
    language_id = db.Column(db.Integer, db.ForeignKey('languages.id'))

    ratings = db.relationship('Rating', backref='text_ratings', lazy='dynamic')

    parent_id = db.Column(db.Integer, db.ForeignKey('texts.id'))
    sons = db.relationship('Text',
                           backref=db.backref('text_sons', remote_side='Text.id'),
                           viewonly=True,
                           lazy='dynamic')

    tags = db.relationship(
        "Tag",
        secondary="tag_text",
        back_populates="texts")

    def __repr__(self):
        return '<Text: {}>'.format(self.text)


