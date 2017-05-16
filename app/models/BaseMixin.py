from app import db
from datetime import datetime
from sqlalchemy.ext.declarative import declared_attr

class BaseMixin(object):

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower() + "s"

    id = db.Column(db.Integer, primary_key=True)

    #created_by = db.Column(db.Integer, db.ForeignKey('lexicographers.id'))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
