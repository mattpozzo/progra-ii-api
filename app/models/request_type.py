from app.models import db
from app.models.audit.base_audit import BaseAudit

class RequestType(BaseAudit):
    __tablename__ = 'request_type'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(128), nullable = False, unique = True))
    body_template = db.Column(db.String(), nullable = False)

    def serialize(self):
        return super().serialize() | {
            "id": self.id,
            "name": self.name,
            "body_template": self.body_template,
        }