from . import db
from app.models.audit.base_audit import BaseAudit

class RecipeIngredient(db.Model, BaseAudit):
    __tablename__ = 'recipe_ingredient'
    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredient.id'), nullable=False)
    quantity = db.Column(db.String(50), nullable=False)


    recipe = db.relationship('Recipe', backref=db.backref('recipe_ingredients', lazy=True))
    ingredient = db.relationship('Ingredient', backref=db.backref('ingredient_recipes', lazy=True))

    def serialize(self):
        return {
            "id": self.id,
            "recipe_id": self.recipe_id,
            "ingredient_id": self.ingredient_id,
            "quantity": self.quantity,
            "recipe": self.recipe.serialize(),
            "ingredient": self.ingredient.serialize(),
        }
