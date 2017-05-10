from app import db
from datetime import datetime

class Language(db.Model):
    # Create a Language table

    __tablename__ = "languages"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    code = db.Column(db.String(6), unique=True)

    words = db.relationship('Word', backref='language',
                                lazy='dynamic')

    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Language: {}>'.format(self.name)
