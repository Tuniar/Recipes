from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from app import app, db
from app.schemas import Recipe, recipe_schema, recipes_schema
import os


# Create a Recipe
@app.route('/recipes', methods=['POST'])
def add_recipe():
  name = request.json['name']
  description = request.json['description']
  image = request.json['image']

  new_recipe = Recipe(name, description, image)

  db.session.add(new_recipe)
  db.session.commit()

  return recipe_schema.jsonify(new_recipe)

# Get All Recipes
@app.route('/recipes', methods=['GET'])
def get_recipes():
  all_recipes = Recipe.query.all()
  result = recipes_schema.dump(all_recipes)
  return jsonify(result)

# Get Single Recipes
@app.route('/recipes/<id>', methods=['GET'])
def get_recipe(id):
  recipe = Recipe.query.get(id)
  return recipe_schema.jsonify(recipe)

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

  return recipe_schema.jsonify(recipe)