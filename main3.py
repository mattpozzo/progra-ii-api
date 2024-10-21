from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy  # es el ORM que permite a la API interactuar con la base de datos de PostgreSQL
from sqlalchemy.exc import IntegrityError  # excepción que lanza SQLAlchemy si se ingresa un dato incorrecto
from apis import api  # Importar la API definida en el paquete apis

# Configuración de Flask y SQLAlchemy
app = Flask(__name__)

# Configurar la base de datos PostgreSQL
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:hola1234T@localhost/PostgresIn10"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  # buena práctica
db = SQLAlchemy(app)  # inicializo la base de datos usando SQLAlchemy

# Definición de la clase User
class User(db.Model):
    __tablename__ = "user"  # El nombre de la tabla dentro de pgAdmin de PostgreSQL (en nuestro db)

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

    def serialize(self):
        '''
        Convierte una instancia de la clase a un formato similar al formato JSON.
        Esto se hace para que la app entienda el mensaje.
        '''
        return {
            "id": self.id,
            "username": self.username
            # No devolveremos la contraseña por razones de seguridad
        }

# Ruta para registrar un nuevo usuario
@app.route('/register', methods=['POST'])
def register_user():
    '''
    Registra un usuario utilizando curl:
    -X POST http://127.0.0.1:5000/register \
    -H "Content-Type: application/json" \
    -d '{"username": "usuario4", "password": "contraseña"}'
    '''
    data = request.get_json()
    new_user = User(username=data['username'], password=data['password'])
    db.session.add(new_user)
    try:
        db.session.commit()
        return jsonify(new_user.serialize()), 201  # Devuelve el usuario registrado
    except IntegrityError:
        db.session.rollback()
        return jsonify({'message': 'Error al registrar el usuario: nombre de usuario ya existe o datos inválidos'}), 400

# Ruta para hacer login
@app.route('/login', methods=['POST'])
def login_user():
    '''
    Función que busca usuarios ya registrados y si existe manda un mensaje.
    Para usarlo:
    hacer login con un usuario utilizando curl:
    -X POST http://127.0.0.1:5000/login \
    -H "Content-Type:application/json" \
    -d '{"username":"usuario4","password":"contraseña"}'
    '''
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()

    if user and user.password == data['password']:
        return jsonify({'message': f'Bienvenido {user.username}'}), 200
    else:
        return jsonify({'message': 'Usuario o contrasena incorrectos'}), 401

# Ruta para obtener todos los usuarios (solo para pruebas)
@app.route('/users', methods=['GET'])
def get_users():
    '''
    Función para obtener los usuarios registrados en la tabla user.
    Para obtenerlos hay que hacer curl:
    -X GET http://127.0.0.1:5000/users
    '''
    users = User.query.all()
    return jsonify([user.serialize() for user in users]), 200  # Devuelve la lista de usuarios

# Inicializamos las rutas de la API
api.init_app(app)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Crea las tablas si no existen
    app.run(debug=True)
