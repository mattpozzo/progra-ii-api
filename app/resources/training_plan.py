from flask_restx import Namespace, Resource
from flask import request
from app.models.models import TrainingPlan, RoutineSchedule
from app.models.models import User
from app.resources.auth.authorize import authorize
from app.models import db
from sqlalchemy.exc import IntegrityError


training_plan_ns = Namespace('training_plan',
                             description=('Operaciones relacionadas '
                                          'con los planes de entrenamiento.'))


@training_plan_ns.route('/')
class GetTrainingPlan(Resource):
    '''Devuelve lista de rutinas asociadas al usuario que lo pide'''
    @authorize
    def get(user: User, self):

        query = TrainingPlan.query.filter_by(user_id=user.id, active=True)
        tr_plans = query.all()
        return [trplan.serialize() for trplan in tr_plans], 200


@training_plan_ns.route('/create/')
class PostTrainingPlan(Resource):
    '''Devuelve lista de rutinas asociadas al usuario que lo pide'''
    @authorize
    def post(user: User, self):
        data = request.get_json()
        description = data.get('description') if 'description' in data else None
        trainee_id = data.get('trainee') if 'trainee' in data else user.id #o lo  creamos para alguien más o lo creamos para nos

        new_trplan = TrainingPlan(
            name=data['name'],
            description=description,
            completed_week=False,
            user_id=trainee_id,
            created_by=user.id
        )
        
        db.session.add(new_trplan)
        db.session.flush()

        routine_schedules = data.get('routine_schedules', [])
        for routine_schedule_data in routine_schedules:
            new_rs = RoutineSchedule(
                weekday=routine_schedule_data['weekday'],
                hour=routine_schedule_data['hour'],
                routine_id=routine_schedule_data['routine_id'],
                training_plan_id=new_trplan.id,
                created_by=user.id
            )
            db.session.add(new_rs)

        try:
            db.session.commit()
            return new_trplan.serialize(), 201
        except IntegrityError:
            db.session.rollback()
            return {'message': 'Database conflict. Please check your input.'}, 409
