from flask_restx import Namespace, Resource
from flask import request
from app.models.models import Trophy, User
from app.models import db

from app.resources.auth.authorize import authorize


trophy_ns = Namespace('trophies', description='Operaciones relacionadas con trofeos')

@trophy_ns.route('/')
class GetTrophies(Resource):
    @authorize
    def get(user: User, self):
        user_id = request.args.get('user', type=int)
        
        # If user is provided, filter by user
        cond = True
        if user_id is not None:
            cond = Trophy.users.any(user_id=user_id)

        trophies = Trophy.query.filter(cond).all()
        return [trophy.serialize() for trophy in trophies], 200

@trophy_ns.route('/<int:id>')
class GetTrophy(Resource):
    @authorize
    def get(user: User, self, id):
        trophy = Trophy.query.filter_by(id=id).first()
        if trophy:
            return trophy.serialize(), 200
        else:
            return {'message': 'Trophy not found.'}, 404