from app.models import db
from app.models.audit.base_audit import BaseAudit

class RequestReceiver(BaseAudit):
    __tablename__ = 'request_receiver'
    id = db.Column(db.Integer, primary_key = True)
    user = db.Column(db.String(128), db.ForeignKey('user.id'))
    request = db.Column(db.String(128), db.ForeignKey('request.id'))

    _user = db.relationship('User', backref = db.backref('requests'), lazy = True)
    _request = db.relationship('Request', backref = db.backref('receivers'), lazy = True)

    def serialize(self):
        return super().serialize() | {
            "id": self.id,
            "user": self._user.serialize(),
            "request": self._request.serialize(),
        }