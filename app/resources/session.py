from flask_restx import Namespace, Resource
from flask import request
from app.models.models import Routine, RoutineExercise, RoutineSchedule, Session
from app.models.models import User
from app.resources.auth.authorize import authorize
from app.models import db
from sqlalchemy.exc import IntegrityError
from sqlalchemy import DateTime, func

session_ns = Namespace('session',
                       description=('Operaciones relacionadas '
                                    'con las sesiones (Historial)'))


@session_ns.route('/')
class GetCurrentSession(Resource):
    '''Devuelve lista de rutinas asociadas al usuario que lo pide'''
    @authorize
    def get(user: User, self):

        current =  (Session.query
                   .filter(Session.user_id == user.id, Session.active == True, Session.duration == None)
                   .all())

        return [session.serialize() for session in current], 200


@session_ns.route('/history')
class GetHistory(Resource):
    '''Devuelve lista de rutinas asociadas al usuario que lo pide'''
    @authorize
    def get(user: User, self):

        history = (
            Session.query
            .filter(Session.user_id == user.id, Session.active == True, Session.duration.isnot(None))
        )

        return [session.serialize() for session in history], 200


