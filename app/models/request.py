from app.models import db
from app.models.audit.base_audit import BaseAudit

class Request(db.Model, BaseAudit):
    __tablename__ = 'request'
    id = db.Column(db.Integer, primary_key = True)
    request_status = db.Column(db.Integer, db.ForeignKey('request_status.id'))
    request_type = db.Column(db.Integer, db.ForeignKey('request_type.id'))
    body = db.Column(db.String(), nullable = False)

    _request_status = db.relationship('RequestStatus', backref = db.backref('requests'), lazy = True)
    _request_type = db.relationship('RequestType', backref = db.backref('requests'), lazy = True)

    def serialize(self):
        return super().serialize() | {
            "id": self.id,
            "request_status": self._request_status.serialize(),
            "request_type": self._request_type.serialize(),
            "body": self.body
        }