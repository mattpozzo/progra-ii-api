from . import db
from app.models.audit.base_audit import BaseAudit

class MealSchedule(db.Model, BaseAudit):
    __tablename__ = 'meal_schedule'

    unique_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    week_day = db.Column(db.Integer, nullable=False)
    hour = db.Column(db.Time, nullable=False)
    training_plan_id = db.Column(db.Integer, nullable=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'),
                          nullable=False)

    recipe = db.relationship('Recipe', backref=db.backref('meal_schedules',
                                                          lazy=True))



    def serialize(self):
        return super().serialize() | {
            "unique_id": self.unique_id,
            "week_day": self.week_day,
            "hour": self.hour.strftime('%H:%M:%S'),  
            "training_plan_id": self.training_plan_id,
            "recipe_id": self.recipe_id,
            "recipe": self.recipe.serialize()  
        }