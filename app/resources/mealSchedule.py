from flask_restx import Namespace, Resource, fields
from flask import request
from app.models.mealSchedule import MealSchedule
from app.models.recipe import Recipe
from app import db

meal_schedule_ns = Namespace('meal_schedules', description='Operaciones relacionadas con los horarios de comidas')

meal_schedule_model = meal_schedule_ns.model('MealSchedule', {
    'unique_id': fields.Integer(readonly=True, description='El ID único del horario'),
    'week_day': fields.String(required=True, description='El día de la semana'),
    'hour': fields.String(required=True, description='La hora en formato HH:MM:SS'),
    'training_plan': fields.String(description='El plan de entrenamiento asociado'),
    'recipe_id': fields.Integer(required=True, description='El ID de la receta asociada')
})

@meal_schedule_ns.route('/')
class MealScheduleListResource(Resource):
    @meal_schedule_ns.expect(meal_schedule_model)
    def post(self):
        '''
        curl -X POST http://localhost:5000/meal_schedules/ \
        -H "Content-Type: application/json" \
        -d '{"week_day": "Monday", "hour": "12:30:00", "training_plan": "Plan A", "recipe_id": 1}'

        '''

        data = request.get_json()
        week_day = data.get('week_day')
        hour = data.get('hour')
        training_plan = data.get('training_plan')
        recipe_id = data.get('recipe_id')

        # Validación
        recipe = Recipe.query.get(recipe_id)
        if not recipe:
            return {'message': 'Recipe not found'}, 404

        # Crear el MealSchedule
        meal_schedule = MealSchedule(
            week_day=week_day,
            hour=hour,
            training_plan=training_plan,
            recipe_id=recipe_id
        )
        db.session.add(meal_schedule)
        db.session.commit()

        return {
            'unique_id': meal_schedule.unique_id,
            'week_day': meal_schedule.week_day,
            'hour': str(meal_schedule.hour),
            'training_plan': meal_schedule.training_plan,
            'recipe_id': meal_schedule.recipe_id
        }, 201

    @meal_schedule_ns.marshal_list_with(meal_schedule_model)
    def get(self):
        meal_schedules = MealSchedule.query.all()  # Obtener todos los horarios de comida
        return meal_schedules  # `marshal_list_with` se encarga de serializar
