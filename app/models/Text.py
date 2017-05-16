from app import db
from .BaseMixin import BaseMixin
import enum

class TextType(enum.Enum):
    Example = 1
    Definition = 2

class Text(BaseMixin, db.Model):

    text = db.Column(db.UnicodeText, unique=True)
    type = db.Column(db.Enum(TextType))

    definition = db.Column(db.Integer, db.ForeignKey('definitions.id'))

    def __repr__(self):
        return '<Text: {}>'.format(self.text)


