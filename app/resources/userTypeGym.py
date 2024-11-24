from flask_restx import Namespace, Resource
from flask import request, current_app
from app.models import db
from app.models.userTypeGym import UserTypeGym
import jwt

user_type_gym_ns = Namespace('user_type_gyms', description='Operaciones relacionadas con la asignación de tipos de usuario a gimnasios')        

# Endpoint para asignar un tipo de usuario a un usuario en un gimnasio (requiere token)
@user_type_gym_ns.route('/assign')
class AssignUserTypeToGym(Resource):
    '''
    curl -X POST http://127.0.0.1:5000/user_type_gyms/assign \
    -H "Authorization: Bearer <token>" \
    -H "Content-Type: application/json" \
    -d '{"user_id": 1, "gym_id": 1, "user_type_id": 1}'
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

            if not all(k in data for k in ['user_id', 'gym_id', 'user_type_id']):
                return {'message': 'Todos los campos (user_id, gym_id, user_type_id) son requeridos'}, 400

            new_assignment = UserTypeGym(
                user_id=data['user_id'],
                gym_id=data['gym_id'],
                user_type_id=data['user_type_id']
            )
            db.session.add(new_assignment)
            db.session.commit()
            return new_assignment.serialize(), 201

        except jwt.ExpiredSignatureError:
            return {'message': 'Token ha expirado, por favor ingresa nuevamente'}, 401
        except jwt.InvalidTokenError:
            return {'message': 'Token invalido'}, 401
        except Exception as e:
            return {'message': f'Error al asignar tipo de usuario a gimnasio: {str(e)}'}, 500




# Endpoint para obtener todas las asignaciones (requiere token)
@user_type_gym_ns.route('/')
class GetUserTypeGyms(Resource):
    '''
    curl -X GET http://127.0.0.1:5000/user_type_gyms/ \
    -H "Authorization: Bearer <token>"
    '''
    def get(self):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return {'message': 'Token requerido'}, 403

        token_parts = auth_header.split()
        if len(token_parts) != 2 or token_parts[0] != 'Bearer':
            return {'message': 'Token invalido'}, 403

        token = token_parts[1]

        try:
            decoded_token = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
            assignments = UserTypeGym.query.all()
            return [assignment.serialize() for assignment in assignments], 200

        except jwt.ExpiredSignatureError:
            return {'message': 'Token expirado'}, 401
        except jwt.InvalidTokenError:
            return {'message': 'Token invalido'}, 401



