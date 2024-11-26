from app.models import db
from app.models.audit.base_audit import BaseAudit


class UserTypeGym(db.Model, BaseAudit):
    __tablename__ = "usertypegym"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    gym_id = db.Column(db.Integer, db.ForeignKey('gym.id'), nullable=False)
    user_type_id = db.Column(db.Integer,
                             db.ForeignKey('usertype.id'),
                             nullable=False)

    user = db.relationship('User',
                           backref=db.backref('user_type_gyms',
                                              lazy=True),
                           foreign_keys=[user_id])
    gym = db.relationship('Gym', backref=db.backref('user_type_gyms',
                                                    lazy=True))
    user_type = db.relationship('UserType',
                                backref=db.backref('user_type_gyms',
                                                   lazy=True))

    def serialize(self):
        return super().serialize() | {
            "id": self.id,
            "user": self.user.serialize(),
            "gym": self.gym.serialize(),
            "user_type": self.user_type.serialize()
        }
