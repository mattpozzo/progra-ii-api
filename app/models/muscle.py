from app.models import db
from app.models.audit.base_audit import BaseAudit
from app.utils import muscles


class Muscle(db.Model, BaseAudit):
    __tablename__ = 'muscle'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False, unique=True)
    description = db.Column(db.String(512))

    def serialize(self):
        return super().serialize() | {
            "id": self.id,
            "name": self.name,
            "description": self.description
        }

