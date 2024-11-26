from . import db


class MealSchedule(db.Model):
    __tablename__ = 'meal_schedule'

    unique_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    week_day = db.Column(db.String(20), nullable=False)  # Ejemplo: "Monday", "Tuesday", etc.
    hour = db.Column(db.Time, nullable=False)  # Hora en formato HH:MM:SS
    training_plan = db.Column(db.String(255), nullable=True)  # Nombre del plan de entrenamiento
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'),
                          nullable=False)  # Relacion con Recipe

    # Relación con Recipe
    recipe = db.relationship('Recipe', backref=db.backref('meal_schedules',
                                                          lazy=True))

    def __repr__(self):
        return f"<MealSchedule(unique_id={self.unique_id}, week_day='{
            self.week_day}', hour={self.hour}, training_plan='{
                self.training_plan}', recipe_id={self.recipe_id})>"
