from flask_restx import Namespace, Resource
from app.models.models import Exercise
from app.models.models import User
from app.resources.auth.authorize import authorize

exercise_ns = Namespace('exercises', description='Operaciones relacionadas con los ejercicios')


@exercise_ns.route('/')
class GetExercises(Resource):
    @authorize
    def get(user: User, self):  # asco but ok?
        exercises = Exercise.query.all()
        return [exercise.serialize() for exercise in exercises], 200
