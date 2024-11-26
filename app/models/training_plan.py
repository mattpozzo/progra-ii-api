from app.models import db
from app.models.audit.base_audit import BaseAudit


class TrainingPlan(db.Model, BaseAudit):
    __tablename__ = 'training_plan'
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.String(512))
    completed_week = db.Column(db.Boolean, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    user = db.relationship('User',
                           backref=db.backref('training_plans',
                                              lazy=True),
                           foreign_keys=[user_id])

    def serialize(self):
        return super().serialize() | {
            "id": self.id,
            'name': self.name,
            'description': self.description,
            'user': self.user.serialize(),
            'completed_week': self.completed_week
        }
