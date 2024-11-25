from flask_restx import Namespace, Resource
from flask import request, current_app
from app.models.user import User
from app.models import db
from sqlalchemy.exc import IntegrityError
import jwt
import datetime
from app.models.training_plan import TrainingPlan
# Crear un namespace para usuarios
user_ns = Namespace('users', description='Operaciones relacionadas con usuarios')



# Clase para registrar usuario
@user_ns.route('/register')
class RegisterUser(Resource):
    '''
    curl -X POST http://127.0.0.1:5000/users/register \
    -H "Content-Type: application/json" \
    -d '{"first_name": "", "last_name": "", "email": "", "password": "", "certified": true}'
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
            return {'message': 'Error al registrar el usuario: email ya existe o datos invalidos'}, 400
        
@user_ns.route('/login')
class LoginUser(Resource):
    '''
    curl -X POST http://127.0.0.1:5000/users/login \
    -H "Content-Type: application/json" \
    -d '{"email": "laura.martinez@example.com", "password": "securepassword123"}'
    DEVUELVE UN TOKEN
    '''
    def post(self):
        tp = TrainingPlan()
        data = request.get_json()
        user = User.query.filter_by(email=data['email']).first()
        if user and user.check_password(data['password']):
            token = jwt.encode({
                'user_id': user.id,
                'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1) #se establece tiempo de duracion del token
            }, current_app.config['SECRET_KEY'], algorithm="HS256")
            return {'token': token}, 200
        else:
            return {'message': 'Usuario o contraseña incorrectos'}, 401

# Clase para obtener todos los usuarios (requiere token de autenticación)
@user_ns.route('/')
class GetUsers(Resource):
    '''
    curl -X GET http://127.0.0.1:5000/users/ \
    -H "Authorization: Bearer <token>"
    '''
    def get(self):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return {'message': 'Token es requerido'}, 403
        
        token_parts = auth_header.split()
        if len(token_parts) != 2 or token_parts[0] != 'Bearer':
            return {'message': 'Token formato invalido'}, 403
        
        token = token_parts[1]

        try:
            decoded_token = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
            users = User.query.all()
            return [user.serialize() for user in users], 200
        except jwt.ExpiredSignatureError:
            return {'message': 'Token ha expirado, por favor ingresa nuevamente'}, 401
        except jwt.InvalidTokenError:
            return {'message': 'Token invalido'}, 401
