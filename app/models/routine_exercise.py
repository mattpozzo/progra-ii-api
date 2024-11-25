from app.models import db
from app.models.audit.base_audit import BaseAudit

class RoutineExercise(db.Model, BaseAudit):
    __tablename__ = 'routine_exercise'
    id = db.Column(db.Integer, primary_key = True)
    sets = db.Column(db.Integer, nullable = False)
    reps = db.Column(db.Integer, nullable = False)
    weight = db.Column(db.Integer, nullable = False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercise.id'), nullable = False)
    notes = db.Column(db.String(512))
    session_id = db.Column(db.Integer, db.ForeignKey('session.id'))
    routine_id = db.Column(db.Integer, db.ForeignKey('routine.id'), nullable = False)

    _exercise = db.relationship('Exercise', backref= db.backref('routine_exercises', lazy=True))
    _session = db.relationship('Session', backref= db.backref('routine_exercise', lazy=True))
    _routine = db.relationship('Routine', backref= db.backref('routine_exercises', lazy=True))

    #que pasaría con el serialize si no hay session?