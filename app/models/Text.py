from app import db
from .BaseMixin import BaseMixin
from .TagText import TagText
from .Rating import Rating
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship, backref
from sqlalchemy import func

import enum

#class TextType(enum.Enum):
#    Example = 2
#    Definition = 1

class Text(BaseMixin, db.Model):

    text = db.Column(db.UnicodeText)
    type = db.Column(db.SmallInteger) #db.Enum(TextType)

    word_id = db.Column(db.Integer, db.ForeignKey('words.id'))
    language_id = db.Column(db.Integer, db.ForeignKey('languages.id'))

    ratings = db.relationship('Rating', backref='text_ratings', lazy='dynamic')

    parent_id = db.Column(db.Integer, db.ForeignKey('texts.id'))
    sons = db.relationship('Text',
                           backref=db.backref('text_sons', remote_side='Text.id'),
                           viewonly=True,
                           lazy='dynamic')

    language = db.relationship('Language', back_populates='texts')

    tags = db.relationship(
        "Tag",
        secondary="tag_text",
        back_populates="texts")

    @hybrid_property
    def num_ratings(self):
        return self.ratings.count()

    @num_ratings.expression
    def _num_ratings_expression(cls):
        return (db.select([db.func.count(Rating.id).label("num_ratings")])
                .where(Rating.text_id == cls.id)
                .label("total_ratings")
                )

    def __repr__(self):
        return '<Text: {}>'.format(self.text)


