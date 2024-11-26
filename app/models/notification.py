from app.models import db
from app.models.audit.base_audit import BaseAudit


class Notification(db.Model, BaseAudit):
    __tablename__ = 'notification'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    body = db.Column(db.String(512), nullable=False)

    def serialize(self):
        return super().serialize() | {
            "id": self.id,
            "title": self.title,
            "body": self.body,
        }
