from app.models import db
from app.models.audit.base_audit import BaseAudit

class UserType(db.Model, BaseAudit):
    __tablename__ = "usertype"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

    def serialize(self):
        return super().serialize() | {
            "id": self.id,
            "name": self.name
        }