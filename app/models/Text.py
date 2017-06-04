from app import db
from .BaseMixin import BaseMixin
from .Relation import Relation
from .Rating import Rating
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship, backref
from sqlalchemy import func

import enum

#class TextType(enum.Enum):
#    Example = 2
#    Definition = 1

class Text(BaseMixin, db.Model):

    text = db.Column(db.UnicodeText)
    type = db.Column(db.SmallInteger) #db.Enum(TextType)
    word_id = db.Column(db.Integer, db.ForeignKey('words.id'))
    language_id = db.Column(db.Integer, db.ForeignKey('languages.id'))

    ratings = db.relationship('Rating', backref='text_ratings', lazy='dynamic')

    # for the examples
    parent_id = db.Column(db.Integer, db.ForeignKey('texts.id'))
    sons = db.relationship('Text',
                           backref=db.backref('text_sons', remote_side='Text.id'),
                           lazy='dynamic')

    language = db.relationship('Language', back_populates='texts')

    tags = db.relationship("Tag", secondary="tag_text", back_populates="texts")

    #relation_to = db.relationship('Relation', backref='to', primaryjoin=id == Relation.text_id_to)
    #relation_from = db.relationship('Relation', backref='from', primaryjoin=id == Relation.text_id_from)

    relations = db.relationship('Relation',
                                secondary=Relation.__table__,
                                primaryjoin="Text.id == Relation.text_id_to",
                                secondaryjoin="Text.id == Relation.text_id_from")

    word = db.relationship("Word", foreign_keys=[word_id])

    # to use as a easy property through the code
    @hybrid_property
    def num_ratings(self):
        return self.ratings.count()

    @num_ratings.expression
    def _num_ratings_expression(cls):
        return (db.select([db.func.count(Rating.id).label("num_ratings")])
                .where(Rating.text_id == cls.id)
                .label("total_ratings")
                )

    def __repr__(self):
        return '<Text: {}>'.format(self.text)


# this relationship is viewonly and selects across the union of all
# friends
relations_union = db.select([
                        Relation.__table__.c.text_id_to,
                        Relation.__table__.c.text_id_from
                        ]).union(
                            db.select([
                                Relation.__table__.c.text_id_to,
                                Relation.__table__.c.text_id_from]
                            )
                    ).alias()

Text.all_relations = relationship('Text',
                       secondary=relations_union,
                       primaryjoin=Text.id==relations_union.c.text_id_to,
                       secondaryjoin=Text.id==relations_union.c.text_id_from,
                       viewonly=True)