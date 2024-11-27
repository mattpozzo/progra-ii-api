from . import db
from app.models.audit.base_audit import BaseAudit

from . import db

class Recipe(db.Model,BaseAudit):
    __tablename__ = 'recipe'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    body = db.Column(db.Text, nullable=True)
    author = db.Column(db.String(255), nullable=True)

   
    ingredients = db.relationship('RecipeIngredient', backref='parent_recipe', lazy=True)


    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "body": self.body,
            "author": self.author, 
            "ingredients": [ingredient.serialize() for ingredient in self.ingredients]
        }