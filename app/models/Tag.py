from app import db
from .BaseMixin import BaseMixin

class Tag(BaseMixin, db.Model):

    tag = db.Column(db.String(30), unique=True, nullable=False)

    texts = db.relationship(
        "Text",
        secondary="tag_text",
        back_populates="tags")

    def __repr__(self):
        return '<Tag: {}>'.format(self.text)