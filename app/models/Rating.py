from app import db
from .BaseMixin import BaseMixin
import enum

class RatingType(enum.Enum):
    Like = 1
    Dislike = 2

class Rating(BaseMixin, db.Model):

    rating = db.Column(db.Enum(RatingType))

    text_id = db.Column(db.Integer, db.ForeignKey('texts.id'))

    def __repr__(self):
        return '<Rating: {}>'.format(self.rating)

