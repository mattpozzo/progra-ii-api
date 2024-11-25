from app.models import db
from app.models.audit.base_audit import BaseAudit

class Session(db.Model, BaseAudit):
    __tablename__ = 'session'
    id = db.Column(db.Integer, primary_key = True)
    date = db.Column(db.Datetime, nulable= False)
    duration = db.Column(db.Interval, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)

    user = db.relationship('User', backref= db.backref('sessions', lazy=True))

    def serialize(self):
        return super().serialize() | {
            "id": self.id,
            "date": self.date,
            "duration": self.duration,
            "user": self.user.serialize()
        }

