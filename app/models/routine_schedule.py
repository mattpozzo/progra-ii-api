from app.models import db
from app.models.audit.base_audit import BaseAudit
from sqlalchemy import Time


class RoutineSchedule(db.Model, BaseAudit):
    __tablename__ = 'routine_schedule'
    id = db.Column(db.Integer, primary_key=True)

    weekday = db.Column(db.Integer, nullable=False)
    hour = db.Column(Time, nullable=False)

    training_plan_id = db.Column(db.Integer, db.ForeignKey('training_plan.id'),
                                 nullable=False)
    routine_id = db.Column(db.Integer, db.ForeignKey('routine.id'),
                           nullable=False)

    training_plan = db.relationship('TrainigPlan',
                                    backref=db.backref('routine_schedules',
                                                       lazy=True))
    routine = db.relationship('Routine')

    def serialize(self):
        return super().serialize() | {
            "id": self.id,
            'weekday': self.weekday,
            'hour': self.hour,
            'training_plan': self.training_plan.serialize(),
            'routine': self.routine.serialize()
        }
