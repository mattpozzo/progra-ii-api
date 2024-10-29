from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash
from flask_restx import Api, Resource, Namespace
import os
import jwt
import datetime

app = Flask(__name__)
api = Api(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://USUARIO:CONTRASEÑA@localhost/BASEDEDATOS"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SECRET_KEY'] = 'tu_secreto_super_secreto'

db = SQLAlchemy(app)

# Clase User
class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    salt = db.Column(db.String(128), nullable=False)
    certified = db.Column(db.Boolean, nullable=False)

    def set_password(self, password):
        self.salt = os.urandom(16).hex()
        self.password_hash = generate_password_hash(password + self.salt)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password + self.salt)

    def serialize(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "certified": self.certified
        }

# Crear un namespace para usuarios
user_ns = Namespace('users', description='Operaciones relacionadas con usuarios')
api.add_namespace(user_ns)

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

# Clase para hacer login y generar un JWT
@user_ns.route('/login')
class LoginUser(Resource):
    '''
    curl -X POST http://127.0.0.1:5000/users/login \
    -H "Content-Type: application/json" \
    -d '{"email": "laura.martinez@example.com", "password": "securepassword123"}'
    DEVUELVE UN TOKEN
    '''
    def post(self):
        data = request.get_json()
        user = User.query.filter_by(email=data['email']).first()
        if user and user.check_password(data['password']):
            token = jwt.encode({
                'user_id': user.id,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
            }, app.config['SECRET_KEY'], algorithm="HS256")
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
            decoded_token = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            users = User.query.all()
            return [user.serialize() for user in users], 200
        except jwt.ExpiredSignatureError:
            return {'message': 'Token ha expirado, por favor ingresa nuevamente'}, 401
        except jwt.InvalidTokenError:
            return {'message': 'Token invalido'}, 401

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)
