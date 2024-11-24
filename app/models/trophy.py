from app.models import db
from app.models.audit.base_audit import BaseAudit

class Trophy(BaseAudit):
    __tablename__ = 'trophy'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(128), nullable = False, unique = True)
    description = db.Column(db.String(512), nullable = False)

    def serialize(self):
        return super().serialize() | {
            "id": self.id,
            "name": self.name,
            "description": self.description,
        }