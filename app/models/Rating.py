from app import db
from .BaseMixin import BaseMixin
import enum

class RatingType(enum.Enum):
    Like = 1
    Dislike = 2

class Rating(BaseMixin, db.Model):

    rating = db.Column(db.Enum(RatingType))

    definition = db.Column(db.Integer, db.ForeignKey('definitions.id'))
    lexicographer = db.Column(db.Integer, db.ForeignKey('lexicographers.id'))

    def __repr__(self):
        return '<Rating: {}>'.format(self.rating)

