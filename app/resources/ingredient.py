from flask_restx import Namespace, Resource
from flask import request, current_app
from app.models import db
from app.models.ingredient import Ingredient



# Crear el namespace
ingredients_ns = Namespace('ingredients', description='Operaciones relacionadas con los ingredientes')

# Crear el recurso relacionado con ingredientes
@ingredients_ns.route('/')
class IngredientResource(Resource):
    def post(self):
        '''
        Crear un ingrediente
        curl -X POST http://localhost:5000/ingredients/ \
        -H "Content-Type: application/json" \
        -d '{"name": "Tomate"}'
        '''
        data = request.get_json()
        name = data.get('name')

        if not name:
            return {'message': 'Name is required'}, 400

        ingredient = Ingredient(name=name)
        db.session.add(ingredient)
        db.session.commit()

        return {'id': ingredient.id, 'name': ingredient.name}, 201

    def get(self):
        '''
        Obtener todos los ingredientes
        curl -X GET http://localhost:5000/ingredients/
        '''
        ingredients = Ingredient.query.all()
        return [{'id': ingredient.id, 'name': ingredient.name} for ingredient in ingredients], 200

@ingredients_ns.route('/<int:id>')  # Define la ruta /ingredients/<id>
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