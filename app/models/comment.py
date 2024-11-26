from app.models import db
from app.models.audit.base_audit import BaseAudit


class Comment(db.Model, BaseAudit):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    comment_id = db.Column(db.Integer, db.ForeignKey('comment.id'))
    body = db.Column(db.String(), nullable=False)

    post = db.relationship('Post', backref=db.backref('comments'), lazy=True)
    comment = db.relationship('Comment',
                              backref=db.backref('comments'),
                              lazy=True)

    def serialize(self):
        return super().serialize() | {
            "id": self.id,
            "post": self.post.serialize(),
            "comment": self.comment.serialize(),
            "body": self.body
        }
