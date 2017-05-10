from app import db
from datetime import datetime

class Word(db.Model):
    # Create a Word table

    __tablename__ = 'words'

    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(60), unique=True)
    definition = db.Column(db.String(200))

    created_by_id = db.Column(db.Integer, db.ForeignKey('lexicographers.id'))
    language_id = db.Column(db.Integer, db.ForeignKey('languages.id'))

    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Word: {}>'.format(self.word)