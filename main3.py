from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash
from flask_restful import Api, Resource
import os

# Configuración de Flask y SQLAlchemy
app = Flask(__name__)
api_restful = Api(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:hola1234T@localhost/PostgresIn10"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


#instanciamos la db
db = SQLAlchemy(app)


# Clase User 
class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)  # Contraseña en texto plano (solo para pruebas)
    password_hash = db.Column(db.String(256), nullable=False)  # Contraseña hasheada
    salt = db.Column(db.String(128), nullable=False)
    certified = db.Column(db.Boolean, nullable=False)

    def set_password(self, password):
        self.password = password  # Guarda la contraseña en texto plano (solo para pruebas)
        self.salt = os.urandom(16).hex()  # Genera un salt único y aleatorio para cada usuario
        self.password_hash = generate_password_hash(password + self.salt)  # Hashea la contraseña

    def check_password(self, password):
        return check_password_hash(self.password_hash, password + self.salt)  # Verifica el hash

    def serialize(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "certified": self.certified
        }



class RegisterUser(Resource):
    '''EJEMPLO DE USO POR TERMINAL
    curl -X POST http://127.0.0.1:5000/register \
    -H "Content-Type: application/json" \
    -d '{"first_name": "Carlos","last_name": "Martinez","email": "carlos.martinez@example.com","password": "contrasena123","certified": true}' 

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
            return {'message': 'Error al registrar el usuario: email ya existe o datos inválidos'}, 400


# Recurso para hacer login
class LoginUser(Resource):
    '''EJEMPLO DE LOGIN
    curl -X POST http://127.0.0.1:5000/login \
    -H "Content-Type: application/json" -d 
    '{"email": "carlos.martinez@example.com", "password": "contrasena123"}'
    '''
    def post(self):
        data = request.get_json()
        user = User.query.filter_by(email=data['email']).first()
        if user and user.check_password(data['password']):
            return {'message': f'Bienvenido {user.first_name} {user.last_name}'}, 200
        else:
            return {'message': 'Usuario o contrasena incorrectos'}, 401



class GetUsers(Resource):
    '''OBTIENE TODOS LOS USUARIOS
    curl GET http:127.0.0.1:5000/users
    '''
    def get(self):
        users = User.query.all()
        return [user.serialize() for user in users], 200  # Flask-RESTful maneja la serialización JSON


# Inicialización de las rutas de la API con Flask-RESTful
api_restful.add_resource(RegisterUser, '/register')
api_restful.add_resource(LoginUser, '/login')
api_restful.add_resource(GetUsers, '/users')

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)
