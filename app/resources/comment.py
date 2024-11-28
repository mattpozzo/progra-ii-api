from flask_restx import Namespace, Resource
from flask import request
from app.models.models import Comment, Gym, Post, Trophy, User
from app.models import db

from app.resources.auth.authorize import authorize


comment_ns = Namespace('comments', description='Operaciones relacionadas con comentarios')

@comment_ns.route('/')
class GetCreateComments(Resource):
    @authorize
    def get(user: User, self):
        post_id = request.args.get('post', type=int)
        comment_id = request.args.get('comment', type=int)
        user_id = request.args.get('user', type=int)
        
        # If user and/or parent are provided, filter by them
        cond = (Comment.active == True, Comment.can_be_read(user))
        if post_id is not None:
            cond += (Comment.post_id == post_id,)
        if comment_id is not None:
            cond += (Comment.comment_id == comment_id,)
        if user_id is not None:
            cond += (Comment.created_by == user_id,)

        comments = Comment.query.filter(*cond).all()
        return [comment.serialize() for comment in comments], 200
    
    @authorize
    def post(user: User, self):
        data = request.json

        # Check if user is a member of the gym
        found_gym = None

        if 'post' in data:
            found_post = Post.query.filter(Post.id == data['post'], Post.active == True).first()

            if not found_post:
                return {'message': 'Post not found.'}, 404
            
            found_gym = found_post.can_be_read(user)
        elif 'comment' in data:
            found_comment = Comment.query.filter(Comment.id == data['comment'], Comment.active == True).first()

            if not found_comment:
                return {'message': 'Comment not found.'}, 404
            
            found_gym = found_comment.can_be_read(user)
        
        if not found_gym:
            return {'message': 'User is not a member of the gym.'}, 403

        new_comment = Comment(
            body=data['body'],
            created_by=user.id,
            post_id=data['post'] if 'post' in data else None,
            comment_id=data['comment'] if 'comment' in data else None
        )
        db.session.add(new_comment)
        db.session.commit()
        return new_comment.serialize(), 201

@comment_ns.route('/<int:id>')
class GetUpdateDeleteComment(Resource):
    @authorize
    def get(user: User, self, id):
        comment = Comment.query.filter_by(id=id, active=True).first()

        if not comment:
            return {'message': 'Comment not found.'}, 404

        if not comment.can_be_read(user):
            return {'message': 'User is not a member of the gym.'}, 403

        return comment.serialize(), 200
        
    @authorize
    def patch(user: User, self, id):
        comment = Comment.query.filter_by(id=id, created_by=user.id, active=True).first()
        if not comment:
            return {'message': 'Comment not found.'}, 404
        
        data = request.json
        comment.body = data.get('body', comment.body)
        db.session.commit()
        return comment.serialize(), 200
    
    @authorize
    def delete(user: User, self, id):
        comment = Comment.query.filter_by(id=id, created_by=user.id).first()
        if not comment:
            return {'message': 'Comment not found.'}, 404
        
        comment.active = False
        db.session.commit()
        return comment.serialize(), 200