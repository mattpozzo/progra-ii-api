from app.models import db
from app.models.audit.base_audit import BaseAudit


class RequestStatus(db.Model, BaseAudit):
    __tablename__ = 'request_status'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False, unique=True)

    def serialize(self):
        return super().serialize() | {
            "id": self.id,
            "name": self.name,
        }
