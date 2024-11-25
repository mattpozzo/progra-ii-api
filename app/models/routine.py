from app.models import db
from app.models.audit.base_audit import BaseAudit


class Routine(db.Model, BaseAudit):
    __tablename__ = 'routine'
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.String(512))

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    gym_id = db.Column(db.Integer, db.ForeignKey('gym.id'))

    _user = db.relationship('User',
                            backref=db.backref('routines',
                                               lazy=True))
    _gym = db.relationship('Gym',
                           backref=db.backref('routines',
                                              lazy=True))

    def serialize(self):
        return super().serialize() | {
            "id": self.id,
            'name': self.name,
            'description': self.description,  # Guarda si es Null,
                                              # podría ser None, PROBAR
            'user': self._user.serialize(),
            'gym': self._gym.serialize() if self._gym else None
        }
