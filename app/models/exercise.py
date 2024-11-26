from app.models import db
from app.models.audit.base_audit import BaseAudit


class Exercise(db.Model, BaseAudit):
    __tablename__ = 'exercise'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False, unique=True)
    description = db.Column(db.String(512))
    muscle = db.Column(db.Integer, db.ForeignKey('muscle.id'), nullable=False)

    muscle = db.relationship('Muscle',
                             backref=db.backref('exercises'),
                             lazy=True)

    def serialize(self):
        return super().serialize() | {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "muscle": self.muscle.serialize()
        }
