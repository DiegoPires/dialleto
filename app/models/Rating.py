from app import db
from .BaseMixin import BaseMixin

class Rating(BaseMixin, db.Model):

    rating = db.Column(db.Integer)

    text_id = db.Column(db.Integer, db.ForeignKey('texts.id'))

    def __repr__(self):
        return '<Rating: {}>'.format(self.rating)

