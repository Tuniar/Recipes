from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from app import app, db, bcrypt
from app.schemas import Recipe, RecipeSchema, RecipeStep, RecipeStepSchema, User, UserSchema
import os

# Create a User
@app.route('/users', methods=['POST'])
def add_user():
  username = request.json['username']
  email = request.json['email']
  password = request.json['password']
  hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
  user_schema = UserSchema()
  user = User(username=username, email=email, password=hashed_password)
  db.session.add(user)
  db.session.commit()

  return jsonify(user_schema.dump(user))


# Create a Recipe
@app.route('/recipes', methods=['POST'])
def add_recipe():
  author_id = request.json['author_id']
  name = request.json['name']
  description = request.json['description']
  image = request.json['image']
  steps = request.json['steps']
  recipe_schema = RecipeSchema()
  new_recipe = Recipe(name, description, image,  author_id)

  db.session.add(new_recipe)
  db.session.commit()

  recipe_id = new_recipe.id

  for step in steps:
    stepnumber = step['stepnumber']
    steptext = step['steptext']
    new_step = RecipeStep(stepnumber, steptext, recipe_id)
    db.session.add(new_step)
    db.session.commit()

  return jsonify(recipe_schema.dump(new_recipe))

# Get All Recipes
@app.route('/recipes', methods=['GET'])
def get_recipes():
  all_recipes = Recipe.query.all()
  recipes_schema = RecipeSchema(many=True)
  output = recipes_schema.dump(all_recipes)
  return jsonify(output)

# Get Single Recipes
@app.route('/recipes/<id>', methods=['GET'])
def get_recipe(id):
  recipe = Recipe.query.get(id)
  recipe_schema = RecipeSchema()
  output = recipe_schema.dump(recipe)
  return jsonify(output)

# Update a Recipe
@app.route('/recipes/<id>', methods=['PUT'])
def update_recipe(id):
  recipe = Recipe.query.get(id)

  name = request.json['name']
  description = request.json['description']
  image = request.json['image']

  recipe.name = name
  recipe.description = description
  recipe.image = image
  db.session.commit()

  return recipe_schema.jsonify(recipe)

# Delete Recipe
@app.route('/recipes/<id>', methods=['DELETE'])
def delete_recipe(id):
  recipe = Recipe.query.get(id)
  db.session.delete(recipe)
  db.session.commit()

  return jsonify(RecipeSchema().dump(recipe))