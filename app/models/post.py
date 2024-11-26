from app.models import db
from app.models.audit.base_audit import BaseAudit


class Post(db.Model, BaseAudit):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True)
    gym_id = db.Column(db.Integer, db.ForeignKey('gym.id'))
    title = db.Column(db.String(128), nullable=False)
    body = db.Column(db.String(), nullable=False)

    gym = db.relationship('Gym', backref=db.backref('posts'), lazy=True)

    def serialize(self):
        return super().serialize() | {
            "id": self.id,
            "gym": self.gym.serialize(),
            "title": self.title,
            "body": self.body
        }
