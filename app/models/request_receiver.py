from app.models import db
from app.models.audit.base_audit import BaseAudit


class RequestReceiver(db.Model, BaseAudit):
    __tablename__ = 'request_receiver'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    request_id = db.Column(db.Integer, db.ForeignKey('request.id'))

    user = db.relationship('User',
                           backref=db.backref('requests'),
                           lazy=True,
                           foreign_keys=[user_id])
    request = db.relationship('Request',
                              backref=db.backref('receivers'),
                              lazy=True)

    def serialize(self):
        return super().serialize() | {
            "id": self.id,
            "user": self.user.serialize(),
            "request": self.request.serialize(),
        }
