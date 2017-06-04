from app import db
from .BaseMixin import BaseMixin

#TypeRelation
#   1=Synonym
#   2=Antonym

class Relation(BaseMixin, db.Model):

    text_id_to = db.Column(db.Integer, db.ForeignKey('texts.id'), primary_key=True)
    text_id_from = db.Column(db.Integer, db.ForeignKey('texts.id'), primary_key=True)

    relations_from = db.relationship("Text", foreign_keys=[text_id_from])
    #relations_child = db.relationship("Text", foreign_keys=[text_id_child])

    type_relation = db.Column(db.Integer)

    def __repr__(self):
        return '<Relation: {}>'.format(self.type_relation)