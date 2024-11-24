from app.models import db
from app.models.audit.base_audit import BaseAudit

class Comment(db.Model, BaseAudit):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key = True)
    post = db.Column(db.String(128), db.ForeignKey('post.id'))
    comment = db.Column(db.String(128), db.ForeignKey('comment.id'))
    body = db.Column(db.String(), nullable = False)

    _post = db.relationship('Post', backref = db.backref('comments'), lazy = True)
    _comment = db.relationship('Comment', backref = db.backref('comments'), lazy = True)

    def serialize(self):
        return super().serialize() | {
            "id": self.id,
            "post": self._post.serialize(),
            "comment": self._comment.serialize(),
            "body": self.body
        }