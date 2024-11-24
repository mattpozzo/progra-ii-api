from app.models import db
from app.models.audit.base_audit import BaseAudit

class UserTrophy(db.Model, BaseAudit):
    __tablename__ = 'user_trophy'
    id = db.Column(db.Integer, primary_key = True)
    user = db.Column(db.Integer, db.ForeignKey('user.id'))
    trophy = db.Column(db.Integer, db.ForeignKey('trophy.id'))

    _user = db.relationship('User', backref = db.backref('trophies'), lazy = True)
    _trophy = db.relationship('Trophy', backref = db.backref('users'), lazy = True)

    def serialize(self):
        return super().serialize() | {
            "id": self.id,
            "trophy": self._trophy.serialize(),
            "user": self._user.serialize()
        }