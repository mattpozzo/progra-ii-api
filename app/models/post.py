from app.models import db
from app.models.audit.base_audit import BaseAudit

class Post(BaseAudit):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key = True)
    gym = db.Column(db.String(128), db.ForeignKey('gym.id'))
    title = db.Column(db.String(128), nullable = False)
    body = db.Column(db.String(), nullable = False)

    _gym = db.relationship('Gym', backref = db.backref('posts'), lazy = True)

    def serialize(self):
        return super().serialize() | {
            "id": self.id,
            "gym": self._gym.serialize(),
            "title": self.title,
            "body": self.body
        }