from app import db, ma
from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow_sqlalchemy.fields import Nested

# User / Account
class User(db.Model):
  id = db.Column(db.Integer, primary_key = True)
  username = db.Column(db.String(20), unique=True, nullable=False)
  email = db.Column(db.String(120), unique=True, nullable=False)
  image_file = db.Column(db.String(20), nullable=False, default='pickle.jpg')
  password = db.Column(db.String(60), nullable=False)
  recipes = db.relationship('Recipe', backref='author', cascade='all,delete')

# Recipe Class/Model
class Recipe(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(100))
  description = db.Column(db.String(200))
  image = db.Column(db.String(20), nullable=False, default='default.jpg')
  steps = db.relationship('RecipeStep', backref='recipe', cascade='all,delete')
  author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

  def __init__(self, name, description, image, author_id):
    self.name = name
    self.description = description
    self.image = image
    self.author_id = author_id

# Steps Class/Model

class RecipeStep(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  stepnumber = db.Column(db.Integer, nullable=False)
  steptext = db.Column(db.Text, nullable=False)
  recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)

  def __init__(self, stepnumber, steptext, recipe_id):
    self.stepnumber = stepnumber
    self.steptext = steptext
    self.recipe_id = recipe_id

# RecipeStep  Schema
class RecipeStepSchema(SQLAlchemyAutoSchema):
  class Meta:
    model = RecipeStep
    include_fk = True
    load_instance = True



# Recipe Schema
class RecipeSchema(SQLAlchemyAutoSchema):
  class Meta:
    model = Recipe
    include_relationships = True
    load_instance = True
  steps = fields.Nested(RecipeStepSchema, many=True)

#User Schema
class UserSchema(SQLAlchemyAutoSchema):
  class Meta:
    model = User
    include_relationships = True
  recipes = fields.Nested(RecipeStepSchema, many=True)
  
