from flask_restx import Namespace, Resource, fields
from flask import request
from app import db
from app.models.models import Review, Recipe, Gym
from app.resources.auth.authorize import authorize  


review_ns = Namespace('reviews', description='Operaciones relacionadas con reseñas')

# Modelo para la reseña (para la documentación de la API)
review_model = review_ns.model('Review', {
    'ID': fields.Integer(readonly=True, description='El ID único de la reseña'),
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

#POST PARA ASIGNAR PUNTUACION A UN GIMNASIO
@review_ns.route('/gym/<int:id>')
class ReviewGymResource(Resource):
    @review_ns.doc('create_review_for_gym')
    @review_ns.expect(review_model)  
    def post(self, id):
        """
        Crear una nueva reseña para un gimnasio.
        curl -X POST http://localhost:5000/reviews/gym/<id> \
        -H "Content-Type: application/json" \
        -d '{"score": 5, "comment": "Excelente gimnasio!"}'
        """
        data = request.get_json()
        score = data.get('score')
        comment = data.get('comment')
        
        
        if not score or not comment:
            return {'message': 'Score and comment are required'}, 400
        
        
        gym = Gym.query.get(id)
        if not gym:
            return {'message': 'Gym not found'}, 404
        
        
        review = Review(score=score, comment=comment, gym_id=id)
        
        
        db.session.add(review)
        db.session.commit()

        return review.serialize(), 201
    

#GET PARA REVIEW POR GIMNASIO Y USUARIO
@review_ns.route('/')
class ReviewListResource(Resource):
    @review_ns.doc('get_reviews')
    def get(self):
        """
        Obtener reseñas filtradas por receta, gimnasio y usuario.
        curl -X GET http://localhost:5000/reviews?recipe=<id>&gym=<id>&user=<id>
        """
        recipe_id = request.args.get('recipe')
        gym_id = request.args.get('gym')
        user_id = request.args.get('user')

        
        query = Review.query

        if recipe_id:
            query = query.filter_by(recipe_id=recipe_id)
        if gym_id:
            query = query.filter_by(gym_id=gym_id)
        if user_id:
            query = query.filter_by(user_id=user_id)

        reviews = query.all()

        return [review.serialize() for review in reviews], 200



# PATCH PARA ACTUALIZAR UNA REVIEW
@review_ns.route('/<int:id>')
class change_review(Resource):
    @review_ns.doc('update_review')
    @review_ns.expect(review_model)  
    def patch(self, id):
        """
        Actualizar una reseña por su ID.
        curl -X PATCH http://localhost:5000/reviews/<id> \
        -H "Content-Type: application/json" \
        -d '{"score": 4, "comment": "Buena receta, pero mejorable."}'
        """
        data = request.get_json()
        score = data.get('score')
        comment = data.get('comment')

        review = Review.query.get(id)
        if not review:
            return {'message': 'Review not found'}, 404

        
        if score is not None:
            review.score = score
        if comment:
            review.comment = comment
        
        db.session.commit()

        return review.serialize(), 200



#ELIMINAR UNA REVIEW
@review_ns.route('/')
class ReviewListResource(Resource):
    @review_ns.doc('get_all_reviews')
    def get(self):
        """
        Obtener todas las reseñas.
        curl -X GET http://localhost:5000/reviews/
        """
        reviews = Review.query.all()

        if not reviews:
            return {'message': 'No reviews found'}, 404

        return [review.serialize() for review in reviews], 200




@review_ns.route('/<int:id>')
class delete_review(Resource):
    @review_ns.doc('delete_review')
    def delete(self, id):
        """
        Eliminar una reseña por su ID.
        curl -X DELETE http://localhost:5000/review/<id>
        """
        review = Review.query.get(id)
        if not review:
            return {'message': 'Review not found'}, 404

        db.session.delete(review)
        db.session.commit()

        return {'message': 'Review deleted successfully'}, 200