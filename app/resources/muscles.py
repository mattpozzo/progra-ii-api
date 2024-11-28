from flask_restx import Namespace, Resource
from app.models.models import Muscle
from app.models.models import User
from app.resources.auth.authorize import authorize

muscle_ns = Namespace('muscles', description='Operaciones relacionadas con los musculos')


@muscle_ns.route('/')
class GetMuscles(Resource):
    @authorize
    def get(user: User, self):  # asco but ok?
        exercises = Muscle.query.all()
        return [exercise.serialize() for exercise in exercises], 200
