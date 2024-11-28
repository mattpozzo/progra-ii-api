from flask_restx import Namespace, Resource
from flask import request
from app.models.models import Routine, RoutineExercise
from app.models.models import User
from app.resources.auth.authorize import authorize
from app.models import db
from sqlalchemy.exc import IntegrityError

routine_ns = Namespace('routine',
                       description=('Operaciones relacionadas '
                                    'con las rutinas'))


@routine_ns.route('/')
class GetRoutines(Resource):
    '''Devuelve lista de rutinas asociadas al usuario que lo pide'''
    @authorize
    def get(user: User, self):

        routines = Routine.query.filter_by(user_id=user.id, active=True).all()
        return [routine.serialize() for routine in routines], 200


@routine_ns.route('/<int:id>/')
class GetUpdateDeleteRoutine(Resource):
    '''Devuelve rutina dado id, si pertenece al usuario'''
    @authorize
    def get(user: User, self,  id):
        routine = Routine.query.filter_by(id=id, user_id=user.id, active=True).first()

        if not routine:
            return {'message': 'Routine not found or not authorized to access this resource.'}, 404

        return routine.serialize(), 200

    @authorize
    def patch(user: User, self,  id):
        routine = Routine.query.filter_by(id=id, user_id=user.id, active=True).first()

        if not routine:
            return {'message': 'Routine not found or not authorized to access this resource.'}, 404

        data = request.get_json()

        routine.name = data.get('name', routine.name)
        routine.description = data.get('description', routine.description)
        routine.updated_by = user.id

        if data.get('routine_exercises') is not None:
            incoming_exercises = data['routine_exercises']
            rtexisting_exercises = {rtexercise.exercise_id: rtexercise for rtexercise in routine.routine_exercises}

            for exercise_data in incoming_exercises:
                if 'exercise_id' in exercise_data and exercise_data['exercise_id'] in rtexisting_exercises:
                    # Actualizar ejercicio existente
                    exercise = rtexisting_exercises[exercise_data['exercise_id']]
                    exercise.sets = exercise_data.get('sets', exercise.sets)
                    exercise.reps = exercise_data.get('reps', exercise.reps)
                    exercise.weight = exercise_data.get('weight', exercise.weight)
                    exercise.notes = exercise_data.get('notes', exercise.notes)
                    exercise.updated_by = user.id
                else:
                    # Crear nuevo ejercicio
                    new_exercise = RoutineExercise(
                        sets=exercise_data['sets'],
                        reps=exercise_data['reps'],
                        weight=exercise_data['weight'],
                        notes=exercise_data.get('notes'),
                        exercise_id=exercise_data['exercise_id'],
                        routine_id=routine.id,
                        created_by=user.id
                    )
                    db.session.add(new_exercise)

        db.session.commit()

        return routine.serialize(), 200

    @authorize
    def delete(user: User, self,  id):
        routine = Routine.query.filter_by(id=id, user_id=user.id, active=True).first()

        if not routine:
            return {'message': 'Routine not found or not authorized to access this resource.'}, 404

        routine.active = False
        routine.updated_by = user.id

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
            user_id=user.id,
            created_by=user.id
        )

        db.session.add(new_routine)
        db.session.flush()

        routine_exercises = data.get('routine_exercises', [])
        for exercise_data in routine_exercises:
            new_exercise = RoutineExercise(
                sets=exercise_data['sets'],
                reps=exercise_data['reps'],
                weight=exercise_data['weight'],
                exercise_id=exercise_data['exercise_id'],
                notes=exercise_data.get('notes'),
                routine_id=new_routine.id,
                created_by=user.id
            )
            db.session.add(new_exercise)

        try:
            db.session.commit()
            return new_routine.serialize(), 201
        except IntegrityError:
            db.session.rollback()
            return {'message': 'Database conflict. Please check your input.'}, 409


@routine_ns.route('/<int:id>/exercises/')
class GetRoutineExercise(Resource):
    '''Devuelve ejercicios para una rutina, dado id, si pertenece al usuario'''
    @authorize
    def get(user: User, self,  id):
        routine = Routine.query.filter_by(id=id, user_id=user.id).first()

        if not routine:
            return {'message': 'Routine not found or not authorized to access this resource.'}, 404

        routine_exercises = routine.routine_exercises

        return [rt_ex.serialize() for rt_ex in routine_exercises], 200
