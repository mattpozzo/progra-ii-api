from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash
from flask_restx import Api, Resource, Namespace, fields
import os
import jwt
import datetime
from dotenv import load_dotenv
import jwt  # Debe ser de la librería PyJWT
import datetime
from dotenv import load_dotenv


app = Flask(__name__) #instancia de flask
api = Api(app)  # instancia de Api de flask_restx, una bifurcación de flask_restful, encargada de crear y organizar las rutas de la API

load_dotenv()
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:hola1234T@localhost/PostgresIn10"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SECRET_KEY'] = 'tu_secreto_super_secreto'

db = SQLAlchemy(app)#instancio la base de datos


# Namespaces
user_type_ns = Namespace('user_types', description='Operaciones relacionadas con los tipos de usuario')
gym_ns = Namespace('gyms', description='Operaciones relacionadas con los gimnasios')
user_trophy_ns = Namespace('user_trophies', description='Operaciones relacionadas con los trofeos de usuarios')
user_type_gym_ns = Namespace('user_type_gyms', description='Operaciones relacionadas con la asignación de tipos de usuario a gimnasios')


# Registro de namespaces

api.add_namespace(user_type_ns)
api.add_namespace(gym_ns)
api.add_namespace(user_trophy_ns)
api.add_namespace(user_type_gym_ns)

#EL TOKEN QUE SE GENERA AL HACER LOGIN SIRVE PARA TODOS LOS <token>
# Clase User
class User(db.Model): #defino un modelo ORM (Object-relational Mapping) que se utiliza para crear una tabla de una base de datos
    #en un codigo en python
    __tablename__ = "user" #creo la tabla user en pgadmin
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
#le agrego el namespace a la API
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
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1) #se establece tiempo de duracion del token
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


# Clase UserType defino la tabla
class UserType(db.Model):
    __tablename__ = "usertype"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name
        }

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


# Clase Gym
class Gym(db.Model):
    __tablename__ = "gym"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    location = db.Column(db.String(120), nullable=True)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "location": self.location
        }



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
            decoded_token = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
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






# Endpoint para listar gimnasios (requiere token)
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
            decoded_token = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            gyms = Gym.query.all()
            return [gym.serialize() for gym in gyms], 200
        except jwt.ExpiredSignatureError:
            return {'message': 'Token ha expirado, por favor ingresa nuevamente'}, 401
        except jwt.InvalidTokenError:
            return {'message': 'Token invalido'}, 401



# Clase UserTypeGym
class UserTypeGym(db.Model):
    __tablename__ = "usertypegym"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    gym_id = db.Column(db.Integer, db.ForeignKey('gym.id'), nullable=False)
    user_type_id = db.Column(db.Integer, db.ForeignKey('usertype.id'), nullable=False)

    user = db.relationship('User', backref=db.backref('user_type_gyms', lazy=True))
    gym = db.relationship('Gym', backref=db.backref('user_type_gyms', lazy=True))
    user_type = db.relationship('UserType', backref=db.backref('user_type_gyms', lazy=True))

    def serialize(self):
        return {
            "id": self.id,
            "user": {
                "id": self.user.id,
                "first_name": self.user.first_name,
                "last_name": self.user.last_name,
                "email": self.user.email
            },
            "gym": {
                "id": self.gym.id,
                "name": self.gym.name,
                "location": self.gym.location
            },
            "user_type": {
                "id": self.user_type.id,
                "name": self.user_type.name
            }
        }



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
            decoded_token = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
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
            decoded_token = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            assignments = UserTypeGym.query.all()
            return [assignment.serialize() for assignment in assignments], 200

        except jwt.ExpiredSignatureError:
            return {'message': 'Token expirado'}, 401
        except jwt.InvalidTokenError:
            return {'message': 'Token invalido'}, 401



# Clase UserTrophy
class UserTrophy(db.Model):
    __tablename__ = "usertrophy"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    trophy_name = db.Column(db.String(80), nullable=False)
    date_awarded = db.Column(db.Date, nullable=True)

    user = db.relationship('User', backref=db.backref('user_trophies', lazy=True))

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "trophy_name": self.trophy_name,
            "date_awarded": self.date_awarded
        }



#INGREDIENTES Y MEALS NUEVAS TABLAS 20/11

# Definir el modelo Ingredient
class Ingredient(db.Model):
    __tablename__ = 'ingredient'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)

# Definir el modelo para la representación JSON (para la documentación)
ingredient_model = api.model('Ingredient', {
    'id': fields.Integer(readonly=True),
    'name': fields.String(required=True)
})

class Recipe(db.Model):
    __tablename__ = 'recipe'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    body = db.Column(db.Text, nullable=True)
    author = db.Column(db.String(255), nullable=True)


#Tabla relacional entre ingredientes y recetas
class RecipeIngredient(db.Model):
    __tablename__ = 'recipe_ingredient'
    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredient.id'), nullable=False)
    quantity = db.Column(db.String(50), nullable=False)

    recipe = db.relationship('Recipe', backref=db.backref('ingredients', lazy=True)) #Permite acceder desde una receta a sus ingredientes
    ingredient = db.relationship('Ingredient', backref=db.backref('recipes', lazy=True)) #Permite acceder desde sus ingredientes a su receta



class Review(db.Model):
    __tablename__ = 'review'
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.Text, nullable=True)
    rating = db.Column(db.Integer, nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)
    author = db.Column(db.String(255), nullable=True)

    recipe = db.relationship('Recipe', backref=db.backref('reviews', lazy=True)) #Permite relacionar las recetas con sus reviews





class MealSchedule(db.Model):
    __tablename__ = 'meal_schedule'
    id = db.Column(db.Integer, primary_key=True)
    week_day = db.Column(db.String(50), nullable=False)
    hour = db.Column(db.Time, nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)

    recipe = db.relationship('Recipe', backref=db.backref('meal_schedules', lazy=True)) #permite relacionar recetas con meal_schedules esto a partir de una referencia inversa
    #a travez de backref



class TrainingPlan(db.Model):  # Modificada para incluir la relación con User
    __tablename__ = 'training_plan'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text, nullable=True)
    completed_weeks = db.Column(db.Integer, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Relación con User

    user = db.relationship('User', backref=db.backref('training_plans', lazy=True))  # Relación ORM




# Ingredientes
# Ruta para crear un ingrediente
# Clase para manejar los ingredientes
class IngredientResource(Resource):
    # POST para crear un nuevo ingrediente
    @api.expect(ingredient_model)  # Espera el modelo para la solicitud POST
    def post(self):
        '''
    Crear un ingrediente
    curl -X POST http://localhost:5000/ingredients \
    -H "Content-Type: application/json" \
    -d '{"name": "Tomate"}'
    '''
        data = request.get_json()  # Obtenemos los datos JSON de la solicitud
        name = data.get('name')  # Extraemos el nombre del ingrediente

        if not name:
            return {'message': 'Name is required'}, 400

        ingredient = Ingredient(name=name)  # Creamos el nuevo ingrediente
        db.session.add(ingredient)  # Lo agregamos a la sesión de la base de datos
        db.session.commit()  # Confirmamos la transacción

        return {'id': ingredient.id, 'name': ingredient.name}, 201  # Retornamos el ingrediente creado en formato JSON

    # GET para obtener todos los ingredientes
    def get(self):
        '''
        obtener todos los ingredientes
         curl -X GET http://localhost:5000/ingredients
        '''
        ingredients = Ingredient.query.all()  # Consulta todos los ingredientes
        return [{'id': ingredient.id, 'name': ingredient.name} for ingredient in ingredients], 200  # Retorna la lista de ingredientes


# Clase para obtener un ingrediente específico por ID
class IngredientByIdResource(Resource):
    # GET para obtener un ingrediente específico por ID
    '''
    curl -X GET http://localhost:5000/ingredients/1
    '''
    
    def get(self, id):
        ingredient = Ingredient.query.get(id)
        if ingredient:
            return {'id': ingredient.id, 'name': ingredient.name}, 200
        else:
            return {'message': 'Ingredient not found'}, 404



api.add_resource(IngredientResource, '/ingredients')  # Para obtener todos los ingredientes y crear nuevos
api.add_resource(IngredientByIdResource, '/ingredients/<int:id>')  # Para obtener un ingrediente por ID
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)
