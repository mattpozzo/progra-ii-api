from . import db
from app.models.audit.base_audit import BaseAudit

class Ingredient(db.Model,BaseAudit):
    __tablename__ = 'ingredient'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)

    def serialize(self):
        return super().serialize() | {
            "id": self.id,
            "name": self.name
        }
