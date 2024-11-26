from functools import wraps
from flask import request, abort
import jwt
import os

from app.config import Config
from app.models.user import User

def authorize(f):
    @wraps(f)
    def decorated_function(*args, **kws):
            if 'Authorization' not in request.headers:
               abort(401)

            user = None
            token = str.replace(str(request.headers['Authorization']), 'Bearer ','')
            try:
                user = User.query.get(jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])['user_id'])
            except:
                abort(401)

            return f(user, *args, **kws)            
    return decorated_function