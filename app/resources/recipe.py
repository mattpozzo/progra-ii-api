from flask_restx import Namespace, Resource, fields
from flask import request
from app import db  # Asegúrate de que db esté configurado correctamente
from app.models.recipe import Recipe  # Asegúrate de importar tu modelo de receta

# Definir el Namespace
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
    @recipe_ns.doc('create_recipe')  # Documenta esta operación
    @recipe_ns.expect(recipe_model)  # Espera el modelo de entrada
    @recipe_ns.marshal_with(recipe_model, code=201)  # Devuelve la receta con el código 201
    def post(self):
        data = request.get_json()
        title = data.get('title')
        description = data.get('description')
        body = data.get('body')
        author = data.get('author')

        # Validación de los datos requeridos
        if not title:
            return {'message': 'Title is required'}, 400

        # Crear la receta
        recipe = Recipe(title=title, description=description, body=body, author=author)
        db.session.add(recipe)
        db.session.commit()

        
        return recipe, 201  # Devuelve la receta creada

# Obtener todas las recetas (GET)
@recipe_ns.route('/')
class RecipeListResource(Resource):
    @recipe_ns.doc('get_recipes')  # Documenta esta operación
    @recipe_ns.marshal_list_with(recipe_model)  # Devuelve una lista de recetas
    def get(self):
        recipes = Recipe.query.all()
        return recipes, 200  
