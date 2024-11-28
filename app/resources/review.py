from flask_restx import Namespace, Resource, fields
from flask import request
from app import db
from app.models.models import Review, Recipe, Gym
from app.resources.auth.authorize import authorize  


review_ns = Namespace('reviews', description='Operaciones relacionadas con reseñas')

# Modelo para la reseña (para la documentación de la API)
review_model = review_ns.model('Review', {
    'UniqueID': fields.Integer(readonly=True, description='El ID único de la reseña'),
    'score': fields.Integer(required=True, description='La calificación de la receta'),
    'comment': fields.String(description='Comentario sobre la receta'),
    'recipe_id': fields.Integer(required=True, description='ID de la receta asociada'),
    'gym_id': fields.Integer(description='ID del gimnasio asociado (opcional)'),
})

# Crear una nueva reseña (POST)
@review_ns.route('/')
class ReviewResource(Resource):
    @authorize  
    @review_ns.doc('create_review') 
    @review_ns.expect(review_model)  
    def post(self, user):
        """
        Crear una nueva reseña.
        curl -X POST http://localhost:5000/reviews/ \
        -H "Content-Type: application/json" \
        -H "Authorization: Bearer <tu_token_jwt>" \
        -d '{"score": 5, "comment": "Excelente receta!", "recipe_id": 1, "gym_id": 2}'
        """
        
        data = request.get_json()
        score = data.get('score')
        comment = data.get('comment')
        recipe_id = data.get('recipe_id')
        gym_id = data.get('gym_id')

        
        if not score or not recipe_id:
            return {'message': 'Score and Recipe ID are required'}, 400

        
        recipe = Recipe.query.get(recipe_id)
        if not recipe:
            return {'message': 'Recipe not found'}, 404

        
        gym = None
        if gym_id:
            gym = Gym.query.get(gym_id)
            if not gym:
                return {'message': 'Gym not found'}, 404

        
        review = Review(score=score, comment=comment, recipe_id=recipe_id, gym_id=gym_id)

        
        db.session.add(review)
        db.session.commit()

        return review.serialize(), 201

# Obtener todas las reseñas de una receta (GET)
@review_ns.route('/recipe/<int:recipe_id>')
class RecipeReviewsResource(Resource):
    @review_ns.doc('get_reviews_by_recipe')
    @review_ns.marshal_list_with(review_model)
    def get(self, recipe_id):
        """
        Obtener todas las reseñas de una receta específica.
        curl -X GET http://localhost:5000/reviews/recipe/1 \
        -H "Authorization: Bearer <tu_token_jwt>"
        """
        reviews = Review.query.filter_by(recipe_id=recipe_id).all()
        return reviews, 200
