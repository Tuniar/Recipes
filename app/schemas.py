from app import db, ma

# Recipe Class/Model
class Recipe(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(100), unique=True)
  description = db.Column(db.String(200))
  image = db.Column(db.String(20), nullable=False, default='default.jpg')

  def __init__(self, name, description, image):
    self.name = name
    self.description = description
    self.image = image

# Recipe Schema
class RecipeSchema(ma.Schema):
  class Meta:
    fields = ('id', 'name', 'description', 'image')

# Init schema
recipe_schema = RecipeSchema()
recipes_schema = RecipeSchema(many=True)