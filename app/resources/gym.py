from flask_restx import Namespace, Resource
from flask import request, current_app
from app.models import db
from app.models.gym import Gym
from app.models.exercise import Exercise
from app.models.muscle import Muscle
import jwt

gym_ns = Namespace('gyms', description='Operaciones relacionadas con los gimnasios')

@gym_ns.route('/')
class GetGyms(Resource):
    '''
    curl -X GET http://127.0.0.1:5000/gyms/ \
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
            gyms = Gym.query.all()
            return [gym.serialize() for gym in gyms], 200
        except jwt.ExpiredSignatureError:
            return {'message': 'Token ha expirado, por favor ingresa nuevamente'}, 401
        except jwt.InvalidTokenError:
            return {'message': 'Token invalido'}, 401



# Endpoint para agregar un gimnasio (requiere token)
@gym_ns.route('/add')
class AddGym(Resource):
    '''
    curl -X POST http://127.0.0.1:5000/gyms/add \
    -H "Authorization: Bearer <token>" \
    -H "Content-Type: application/json" \
    -d '{"name": "San Martin", "location": "San Martin"}'
    '''
    def post(self):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return {'message': 'Token es requerido'}, 403

        token_parts = auth_header.split()
        if len(token_parts) != 2 or token_parts[0] != 'Bearer':
            return {'message': 'Token formato invalido'}, 403

        token = token_parts[1]

        try:
            decoded_token = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
            data = request.get_json()

            if 'name' not in data:
                return {'message': 'El nombre del gimnasio es requerido'}, 400

            new_gym = Gym(
                name=data['name'],
                location=data.get('location')
            )
            db.session.add(new_gym)
            db.session.commit()
            return new_gym.serialize(), 201

        except jwt.ExpiredSignatureError:
            return {'message': 'Token ha expirado, por favor ingresa nuevamente'}, 401
        except jwt.InvalidTokenError:
            return {'message': 'Token invalido'}, 401
        except Exception as e:
            return {'message': f'Error al agregar gimnasio: {str(e)}'}, 500
