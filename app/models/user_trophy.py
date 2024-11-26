from app.models import db
from app.models.audit.base_audit import BaseAudit


class UserTrophy(db.Model, BaseAudit):
    __tablename__ = 'user_trophy'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    trophy_id = db.Column(db.Integer, db.ForeignKey('trophy.id'))

    user = db.relationship('User',
                           backref=db.backref('trophies'),
                           lazy=True,
                           foreign_keys=[user_id])
    trophy = db.relationship('Trophy',
                             backref=db.backref('users'),
                             lazy=True)

    def serialize(self):
        return super().serialize() | {
            "id": self.id,
            "trophy": self.trophy.serialize(),
            "user": self.user.serialize()
        }
