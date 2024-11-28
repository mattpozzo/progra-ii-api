from flask_restx import Namespace, Resource, fields
from flask import request
from app import db  
from app.models.models import Recipe , RecipeIngredient, Ingredient 
from app.models.models import User
from app.resources.auth.authorize import authorize
recipe_ns = Namespace('recipes', description='Operaciones relacionadas con recetas')

# Definir el modelo de receta para la API
recipe_model = recipe_ns.model('Recipe', {
    'id': fields.Integer(readonly=True, description='El ID único de la receta'),
    'title': fields.String(required=True, description='El título de la receta'),
    'description': fields.String(description='Una descripción breve de la receta'),
    'body': fields.String(description='Las instrucciones detalladas de la receta'),
    'author': fields.String(description='El creador de la receta'),
})

# Crear una nueva receta (POST)
@recipe_ns.route('/')
class RecipeResource(Resource):
    @authorize  
    @recipe_ns.doc('create_recipe') 
    @recipe_ns.expect(recipe_model)  
    @recipe_ns.marshal_with(recipe_model, code=201) 
    def post(self, user: User):
        '''Agregar una nueva receta
        curl -X POST http://localhost:5000/recipes/ \
        -H "Content-Type: application/json" \
        -H "Authorization: Bearer <tu_token_jwt>" \
        -d '{"title": "Milanesa", "description": "Milanesa y papas fritas", "body": "Instrucciones detalladas", "author": "Chef bau"}'
        '''
        # Obtener los datos del cuerpo de la solicitud
        data = request.get_json()
        title = data.get('title')
        description = data.get('description')
        body = data.get('body')
        author = data.get('author')

        # Validar que el título esté presente
        if not title:
            return {'message': 'Title is required'}, 400

        # Crear la receta con los datos proporcionados
        recipe = Recipe(title=title, description=description, body=body, author=author)

        # No asignar created_by (ya no usamos set_created_by)

        # Agregar la receta a la base de datos
        db.session.add(recipe)
        db.session.commit()

        # Devolver la receta creada con el código 201
        return recipe, 201



# Crear una nueva receta (POST)
@recipe_ns.route('/<int:recipe_id>/ingredients')
class RecipeIngredientResource(Resource):
    def post(self, recipe_id):
        '''
        Agregar un ingrediente a una receta
        curl -X POST http://localhost:5000/recipes/1/ingredients \
        -H "Content-Type: application/json" \
        -d '{"ingredient_id": 2, "quantity": "100g"}'
        '''
        data = request.get_json()
        ingredient_id = data.get('ingredient_id')
        quantity = data.get('quantity')

        if not ingredient_id or not quantity:
            return {'message': 'Ingredient ID and quantity are required'}, 400

        # Obtener la receta y el ingrediente
        recipe = Recipe.query.get(recipe_id)
        ingredient = Ingredient.query.get(ingredient_id)

        if not recipe or not ingredient:
            return {'message': 'Recipe or Ingredient not found'}, 404

        # Verificar si el ingrediente ya está asociado a la receta
        existing_recipe_ingredient = RecipeIngredient.query.filter_by(
            recipe_id=recipe_id, ingredient_id=ingredient_id).first()

        if existing_recipe_ingredient:
            return {'message': f'Ingredient "{ingredient.name}" already exists in this recipe.'}, 400

        # Crear la relación en RecipeIngredient
        recipe_ingredient = RecipeIngredient(
            recipe_id=recipe_id,
            ingredient_id=ingredient_id,
            quantity=quantity
        )
        db.session.add(recipe_ingredient)
        db.session.commit()

        return {
            'recipe_id': recipe_ingredient.recipe_id,
            'ingredient_id': recipe_ingredient.ingredient_id,
            'quantity': recipe_ingredient.quantity
        }, 201







# Obtener todas las recetas (GET)
@recipe_ns.route('/')
class RecipeListResource(Resource):
    @authorize  
    @recipe_ns.doc('get_recipes') 
    @recipe_ns.marshal_list_with(recipe_model) 
    def get(self, user: User):
        '''Obtener todas las recetas
        curl -X GET http://localhost:5000/recipes/ \
        -H "Authorization: Bearer <tu_token_jwt>"
        '''
        
        recipes = Recipe.query.all()

        
        return recipes, 200



    
@recipe_ns.route('/<int:recipe_id>')
class RecipeDetailResource(Resource):
    @authorize
    def get(self, user: User, recipe_id):
        """
        Obtener los detalles de una receta junto con sus ingredientes.
        curl -X GET http://localhost:5000/recipes/1 \
        -H "Authorization: Bearer <tu_token_jwt>"
        """
        
        recipe = Recipe.query.get(recipe_id)
        if not recipe:
            return {'message': 'Recipe not found'}, 404

        
        ingredients = RecipeIngredient.query.filter_by(recipe_id=recipe_id).all()

        
        ingredients_data = [
            {
                'ingredient_id': ri.ingredient_id,
                'name': ri.ingredient.name,
                'quantity': ri.quantity
            } for ri in ingredients
        ]

        
        recipe_data = {
            'id': recipe.id,
            'title': recipe.title,
            'description': recipe.description,
            'body': recipe.body,
            'author': recipe.author,
            'ingredients': ingredients_data
        }

        return recipe_data, 200
