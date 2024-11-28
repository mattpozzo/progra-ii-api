from flask_restx import Namespace, Resource
from flask import request
from app.models.models import Exercise, RoutineExercise
from app.models.models import User
from app.resources.auth.authorize import authorize

exercise_ns = Namespace('exercises',
                        description=('Operaciones relacionadas '
                                     'con los ejercicios'))


@exercise_ns.route('/')
class GetExercises(Resource):
    @authorize
    def get(user: User, self):  # asco but ok?
        muscle_id = request.args.get('muscle', type=int)
        cond = True
        if muscle_id is not None:
            cond = Exercise.muscle.has(id=muscle_id)

        exercises = Exercise.query.filter(cond).all()
        return [exercise.serialize() for exercise in exercises], 200

