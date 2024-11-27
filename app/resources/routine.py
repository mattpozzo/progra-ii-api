from flask_restx import Namespace, Resource
from flask import request
from app.models.models import Routine
from app.models.models import User
from app.resources.auth.authorize import authorize
from app.models import db
from sqlalchemy.exc import IntegrityError

routine_ns = Namespace('routine',
                       description=('Operaciones relacionadas '
                                    'con las rutinas'))


@routine_ns.route('/')
class GetRoutines(Resource):
    @authorize
    def get(user: User, self):  # asco but ok?
        # muscle_id = request.args.get('muscle', type=int)
        # cond = True
        # if muscle_id is not None:
        cond = Routine.user_id == user.id

        routines = Routine.query.filter(cond).all()
        return [routine.serialize() for routine in routines], 200


@routine_ns.route('/<int:id>/')
class GetUpdateDeleteRoutine(Resource):
    @authorize
    def get(user: User, self,  id):
        routine = Routine.query.filter_by(id=id, user_id=user.id).first()

        if not routine:
            return {'message': 'Routine not found or not authorized to access this resource.'}, 404

        return routine.serialize(), 200

    @authorize
    def patch(user: User, self,  id):
        routine = Routine.query.filter_by(id=id, user_id=user.id).first()

        if not routine:
            return {'message': 'Routine not found or not authorized to access this resource.'}, 404

        data = request.get_json()

        routine.name = data.get('name', routine.name)
        routine.description = data.get('description', routine.description)
        # ver que hacer con los routine exercise!!

        db.session.commit()

        return routine.serialize(), 200

    @authorize
    def delete(user: User, self,  id):
        routine = Routine.query.filter_by(id=id, user_id=user.id).first()

        if not routine:
            return {'message': 'Routine not found or not authorized to access this resource.'}, 404

        db.session.delete(routine)

        db.session.commit()

        return routine.serialize(), 200

@routine_ns.route('/create/')
class PostRoutine(Resource):
    @authorize
    def post(user: User, self):
        data = request.get_json()
        description = data.get('description') if 'description' in data else None
        gym_id = data.get('gym_id') if 'gym_id' in data else None

        new_routine = Routine(
            name=data['name'],
            description=description,
            gym_id=gym_id,
            user_id=user.id
        )

        db.session.add(new_routine)
        try:
            db.session.commit()
            return new_routine.serialize(), 201
        except IntegrityError:
            db.session.rollback()
            return {'message': 'Error al registrar el usuario: email ya existe o datos invalidos.'}, 409
        
