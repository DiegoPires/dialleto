from app import db

class TagText(db.Model):

    __tablename__ = "tag_text"

    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)
    text_id = db.Column(db.Integer, db.ForeignKey('texts.id'), primary_key=True)

    tag = db.relationship("Tag", backref=db.backref("tag_texts", cascade="all, delete-orphan"))
    text = db.relationship("Text", backref=db.backref("tag_texts", cascade="all, delete-orphan"))

    def __repr__(self):
        return '<TagText: {}>'.format(self.tag.tag+""+ self.text.text)