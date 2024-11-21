from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api
from .config import Config
from .models import db
from .resources.user import user_ns
from .resources.gym import gym_ns
from .resources.usertype import user_type_ns
from .resources.userTypeGym import user_type_gym_ns
from .resources.ingredient import ingredients_ns
from .resources.recipe import recipe_ns



def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    api = Api(app, title="My Flask App API", version="1.0", description="A sample API")
    api.add_namespace(user_ns)
    api.add_namespace(gym_ns)
    api.add_namespace(user_type_ns)
    api.add_namespace(user_type_gym_ns)
    api.add_namespace(ingredients_ns)
    api.add_namespace(recipe_ns)
     
    with app.app_context():
        db.create_all()

    return app
