from app import db
from datetime import datetime
from sqlalchemy.ext.declarative import declared_attr

class BaseMixin(object):

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower() + "s"

    @declared_attr
    def created_by_id(cls):
        return db.Column(db.Integer, db.ForeignKey('lexicographers.id'))

    id = db.Column(db.Integer, primary_key=True)

    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

