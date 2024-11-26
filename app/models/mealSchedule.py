from . import db


class MealSchedule(db.Model):
    __tablename__ = 'meal_schedule'

    unique_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    week_day = db.Column(db.Integer, nullable=False)
    hour = db.Column(db.Time, nullable=False)
    training_plan_id = db.Column(db.Integer, nullable=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'),
                          nullable=False)

    recipe = db.relationship('Recipe', backref=db.backref('meal_schedules',
                                                          lazy=True))
