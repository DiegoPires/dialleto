from app import db
from datetime import datetime
from sqlalchemy.ext.declarative import declared_attr
from ..models.SuperMixin import SuperMixin

class BaseMixin(SuperMixin):


    @declared_attr
    def created_by_id(cls):
        return db.Column(db.Integer, db.ForeignKey('lexicographers.id'))

    @declared_attr
    def lexicographer(cls):
        return db.relationship("Lexicographer", back_populates=cls.__tablename__)





