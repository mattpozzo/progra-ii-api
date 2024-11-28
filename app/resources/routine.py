from flask_restx import Namespace, Resource
from flask import request
from app.models.models import Routine, RoutineExercise, RoutineSchedule, Session
from app.models.models import User
from app.resources.auth.authorize import authorize
from app.models import db
from sqlalchemy.exc import IntegrityError
from sqlalchemy import DateTime, func

routine_ns = Namespace('routine',
                       description=('Operaciones relacionadas '
                                    'con las rutinas'))


@routine_ns.route('/')
class GetRoutines(Resource):
    '''Devuelve lista de rutinas asociadas al usuario que lo pide'''
    @authorize
    def get(user: User, self):
        training_plan_id = request.args.get('training_plan_id', type=int)

        query = Routine.query.filter_by(user_id=user.id, active=True)

        if training_plan_id is not None:
            query = query.join(RoutineSchedule).filter(
                RoutineSchedule.training_plan_id == training_plan_id
                )

        # Fetch filtered routines
        routines = query.all()
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
        routine = Routine.query.filter_by(id=id, user_id=user.id, active=True).first()

        if not routine:
            return {'message': 'Routine not found or not authorized to access this resource.'}, 404

        routine_exercises = routine.routine_exercises

        return [rt_ex.serialize() for rt_ex in routine_exercises], 200


@routine_ns.route('/templates/')
class GetTemplateRoutines(Resource):
    '''Devuelve ejercicios para una rutina, dado id, si pertenece al usuario'''
    @authorize
    def get(user: User, self):

        # Subquery to find all routines with a RoutineSchedule
        subquery = db.session.query(RoutineSchedule.routine_id).distinct()

        # Query routines for the user, excluding those in the subquery
        routines = Routine.query.filter(
            Routine.user_id == user.id,
            Routine.active == True,
            ~Routine.id.in_(subquery)  # Exclude routines with a RoutineSchedule
        ).all()

        # Handle no results
        if not routines:
            return {'message': 'No template routines found for the user.'}, 404

        # Serialize and return results
        return [routine.serialize() for routine in routines], 200


@routine_ns.route('/<int:id>/train/')
class PostRoutineSession(Resource):

    @authorize
    def post(user: User, self, id):

        session = Session.query.filter_by(user_id=user.id, duration=None, active=True).first()

        if session is None:
            # Sin ongiong, crear
            session = Session(
                user_id=user.id,
                created_by=user.id
            )

            db.session.add(session)
            db.session.flush()

            routine = Routine.query.filter_by(user_id=user.id, id=id).first()
            templates = routine.routine_exercises
            templates = RoutineExercise.query.filter_by(created_by=user.id, routine_id=id, session_id=None)

            res = []

            for template in templates:

                new_rtex = RoutineExercise(
                    sets=template.sets,
                    reps=template.reps,
                    weight=template.weight,
                    exercise_id=template.exercise_id,
                    notes=template.notes,
                    routine_id=template.routine_id,
                    created_by=user.id,
                    session_id=session.id
                )

                res.append(new_rtex)

                db.session.add(new_rtex)

            db.session.commit()

            return {'exercises_done': [re.serialize() for re in res]}, 201
        
        else:
            # routine = Routine.query.filter_by(user_id=user.id, active=True).first()
            query = RoutineExercise.query.filter(
                RoutineExercise.session_id == session.id
                ).all()
            
            if not query:
                #user is currently training with a different routine!
                return {'message': 'ERROR: user is already training with different routine!'}
            
            data = request.get_json()

            if not data:
                return {'message': 'ERROR: trying to end a session without providing the exercises made!'}
            
            rtex_dict = dict()

            for exercise in data['routine_exercises']:
                #la idea es, a partir de rtex en json, hacer dict id: rtex.
                #con ese dict, itero sobre query (son los rtex creados anteriormente)
                #que si tienen session id, y los modifico en función de su id.
                rtex_dict[exercise['exercise_id']] = exercise

            rtex_list_og = []
            for rtex in query:
                data_rtex = rtex_dict[rtex.exercise_id]
                rtex.sets = data_rtex.get('sets', rtex.sets)
                rtex.reps = data_rtex.get('reps', rtex.reps)
                rtex.weight = data_rtex.get('weight', rtex.weight)
                rtex.notes = data_rtex.get('notes', rtex.notes)
                rtex_list_og.append(rtex)

            session.duration = func.now() - session.created_at

            db.session.commit()

            return {'session_duration': str(session.duration),
                    'exercises_done': [rtex.serialize() for rtex in rtex_list_og]}, 201
    


        



