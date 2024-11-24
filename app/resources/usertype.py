from flask_restx import Namespace, Resource
from flask import request
from app.models.usertype import UserType
from app.models import db

user_type_ns = Namespace('user_types', description='Operaciones relacionadas con los tipos de usuario')

@user_type_ns.route('/add')
class AddUserType(Resource):
    '''
    curl -X POST http://127.0.0.1:5000/user_types/add \
    -H "Content-Type: application/json" \
    -d '{"name": "New UserType"}'
    '''
    def post(self):
        data = request.get_json()  # Obtener los datos del cuerpo de la solicitud
        new_user_type = UserType(name=data['name'])  # Crear una nueva instancia de UserType

        try:
            db.session.add(new_user_type)  # Agregar a la sesión de la base de datos
            db.session.commit()  # Confirmar los cambios
            return new_user_type.serialize(), 201  # Retornar el nuevo tipo de usuario creado
        except Exception as e:
            db.session.rollback()  # En caso de error, deshacer los cambios
            return {'message': f'Error al agregar tipo de usuario: {str(e)}'}, 400



@user_type_ns.route('/')
class GetUserTypes(Resource):
    '''
    curl -X GET http://127.0.0.1:5000/user_types/
    '''
    def get(self):
        # Lógica para obtener los tipos de usuario
        user_types = UserType.query.all()  # Obtén todos los tipos de usuario de la base de datos
        return [user_type.serialize() for user_type in user_types], 200  # Retorna los tipos de usuario serializados