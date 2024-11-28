from flask_restx import Namespace, Resource
from flask import request
from app.models.models import Gym, Post, Trophy, User
from app.models import db

from app.resources.auth.authorize import authorize


post_ns = Namespace('posts', description='Operaciones relacionadas con posts')

@post_ns.route('/')
class GetCreatePosts(Resource):
    @authorize
    def get(user: User, self):
        gym_id = request.args.get('gym', type=int)
        user_id = request.args.get('user', type=int)
        
        # If user and/or gym are provided, filter by them
        cond = (Post.active == True, Post.can_be_read(user))
        if gym_id is not None:
            cond += (Post.gym_id == gym_id,)
        if user_id is not None:
            cond += (Post.created_by == user_id,)

        posts = Post.query.filter(*cond).all()
        return [post.serialize() for post in posts], 200
    
    @authorize
    def post(user: User, self):
        data = request.json

        # Check if user is a member of the gym
        found_gym = Gym.query.filter(Gym.id == data['gym'], Gym.users.any(user_id=user.id)).first()
        if not found_gym:
            return {'message': 'User is not a member of the gym.'}, 403

        new_post = Post(
            title=data['title'],
            body=data['body'],
            created_by=user.id,
            gym_id=data['gym']
        )
        db.session.add(new_post)
        db.session.commit()
        return new_post.serialize(), 201

@post_ns.route('/<int:id>')
class GetUpdateDeletePost(Resource):
    @authorize
    def get(user: User, self, id):
        post = Post.query.filter_by(id=id, active=True).first()

        if not post:
            return {'message': 'Post not found.'}, 404
        
        if not post.can_be_read(user):
            return {'message': 'User is not a member of the gym.'}, 403

        return post.serialize(), 200
        
    @authorize
    def patch(user: User, self, id):
        post = Post.query.filter_by(id=id, active=True).first()

        if not post:
            return {'message': 'Post not found.'}, 404
        
        if post.created_by != user.id:
            return {'message': 'User cannot modify the post.'}, 403
        
        data = request.json
        post.title = data.get('title', post.title)
        post.body = data.get('body', post.body)
        db.session.commit()
        return post.serialize(), 200
    
    @authorize
    def delete(user: User, self, id):
        post = Post.query.filter_by(id=id, active=True).first()

        if not post:
            return {'message': 'Post not found.'}, 404
        
        if post.created_by != user.id:
            return {'message': 'User cannot delete the post.'}, 403
        
        post.active = False
        db.session.commit()
        return post.serialize(), 200