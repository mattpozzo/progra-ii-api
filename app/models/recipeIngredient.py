from . import db


class RecipeIngredient(db.Model):
    __tablename__ = 'recipe_ingredient'
    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer,
                          db.ForeignKey('recipe.id'),
                          nullable=False)
    ingredient_id = db.Column(db.Integer,
                              db.ForeignKey('ingredient.id'),
                              nullable=False)
    quantity = db.Column(db.String(50), nullable=False)

    recipe = db.relationship('Recipe', backref=db.backref('ingredients',
                                                          lazy=True))
    ingredient = db.relationship('Ingredient', backref=db.backref('recipes',
                                                                  lazy=True))
