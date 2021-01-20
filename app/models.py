from datetime import datetime
from app import db, login_manager
from sqlalchemy.inspection import inspect
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
  return User.query.get(int(user_id))

class Serializer(object):

    def serialize(self):
        return {c: getattr(self, c) for c in inspect(self).attrs.keys()}

    @staticmethod
    def serialize_list(l):
        return [m.serialize() for m in l]

class User(db.Model, UserMixin, Serializer):
  id = db.Column(db.Integer, primary_key = True)
  username = db.Column(db.String(20), unique=True, nullable=False)
  email = db.Column(db.String(120), unique=True, nullable=False)
  image_file = db.Column(db.String(20), nullable=False, default='pickle.jpg')
  password = db.Column(db.String(60), nullable=False)
  recipes = db.relationship('Recipe', backref='author', lazy=True)

  def __repr__(self):
    return f"User('{self.username}', '{self.email}', '{self.image_file}'"



class Recipe(db.Model, Serializer):
  id = db.Column(db.Integer, primary_key=True)
  recipename = db.Column(db.String(20), nullable=False)
  recipedesc = db.Column(db.String(100), nullable=False)
  createddate = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
  image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
  steps = db.relationship('RecipeStep', backref='recipe', lazy=False)
  ingredients = db.relationship('RecipeIngredient', backref='recipe', lazy=False)
  author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

  def __repr__(self):
    return f"Recipes {self.recipename}"

class RecipeStep(db.Model, Serializer):
  id = db.Column(db.Integer, primary_key=True)
  stepnumber = db.Column(db.Integer, nullable=False)
  steptext = db.Column(db.Text, nullable=False)
  recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)

  def __repr__(self):
    return f"Recipe {self.recipe_id}, Step {self.stepnumber}"

class Ingredient(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.Text, nullable=False)
  image_file = db.Column(db.String(20))
  recipes = db.relationship('RecipeIngredient', backref='ingredient', lazy=False)

  def __repr__(self):
    return f"Ingredient {self.name}"

class RecipeIngredient(db.Model, Serializer):
  id = db.Column(db.Integer, primary_key=True)
  recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)
  ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredient.id'), nullable=False)
  unit_id = db.Column(db.Integer, db.ForeignKey('unit.id'), nullable=False)
  amount = db.Column(db.Integer, nullable=False)

  def __repr__(self):
    return f"Link between recipe {self.recipe_id} and ingredient {self.ingredient_id}. Measured in {self.unit}"

class Unit(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.Text, nullable=False)
  ingredients = db.relationship('RecipeIngredient', backref='unit', lazy=False)
  def __repr__(self):
    return f"Unit {self.name}"

