from flask_restx import Namespace, Resource
from flask import request, current_app
from app.models.models import User
from app.models import db
from sqlalchemy.exc import IntegrityError
import jwt
import datetime

from app.resources.auth.authorize import authorize


# Crear un namespace para usuarios
user_ns = Namespace('users', description='Operaciones relacionadas con usuarios')



user_ns = Namespace('users', description='Operaciones relacionadas con usuarios')


user_ns = Namespace('users', description='Operaciones relacionadas con usuarios')


@user_ns.route('/register')
class RegisterUser(Resource):
    '''
    curl -X POST http://localhost:5000/users/register \
    -H "Content-Type: application/json" \
    -d '{"first_name": "hola", "last_name": "hola", "email": "hola@a.com", "password": "asd", "certified": true}'

    '''
    def post(self):
        data = request.get_json()
        new_user = User(
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email'],
            certified=data.get('certified', False)
        )
        new_user.set_password(data['password'])
        db.session.add(new_user)
        try:
            db.session.commit()
            return new_user.serialize(), 201
        except IntegrityError:
            db.session.rollback()
            return {'message': 'Error al registrar el usuario: email ya existe o datos invalidos.'}, 409
        
@user_ns.route('/login')
class LoginUser(Resource):
    def post(self):
        '''
    curl -X POST http://localhost:5000/users/login \
    -H "Content-Type: application/json" \
    -d '{"email": "hola@a.com", "password": "asd"}' DEVUELVE TOKEN

    '''
        data = request.get_json()
        user = User.query.filter_by(email=data['email']).first()
        if user and user.check_password(data['password']):
            token = jwt.encode({
                'user_id': user.id,
                'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1) #se establece tiempo de duracion del token
            }, current_app.config['SECRET_KEY'], algorithm="HS256")
            return {'token': token}, 200
        else:
            return {'message': 'Usuario o contraseña incorrectos.'}, 401

@user_ns.route('/')
class GetUsers(Resource):
    @authorize
    def get(user: User, self):
        gym_id = request.args.get('gym', type=int)

        
        # If gym is provided, filter by gym
        cond = True
        if gym_id is not None:
            cond = User.gyms.any(gym_id=gym_id)

        users = User.query.filter(cond).all()
        return [user.serialize() for user in users], 200

@user_ns.route('/<int:id>')
class GetUpdateUser(Resource):
    @authorize
    def get(user: User, self, id):
        user = User.query.filter_by(id=id).first()
        if user:

            return user.serialize(), 200
        else:
            return {'message': 'User not found.'}, 404
        
    @authorize
    def patch(user: User, self, id):
        if user.id != id:
            return {'message': 'No tienes permiso para modificar este usuario.'}, 403
        

        data = request.json
        user.first_name = data.get('first_name', user.first_name)
        user.last_name = data.get('last_name', user.last_name)

        # Validates email
        email = data.get('email', user.email)
        if email != user.email:
            repeated_email = User.query.filter(User.email == email).first()

            if repeated_email:
                return {'message': 'El email ingresado ya está tomado.'}, 409

            user.email = email
        
        db.session.commit()
        return user.serialize(), 200