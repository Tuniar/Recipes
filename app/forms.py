from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import Form, StringField, SubmitField, FileField, IntegerField, TextAreaField, PasswordField, BooleanField, FieldList, FormField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import User, Unit, Ingredient

class RegistrationForm(FlaskForm):
  username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
  email = StringField('Email', validators=[DataRequired(), Email()])
  password = PasswordField('Password', validators=[DataRequired()])
  confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
  submit = SubmitField('Sign Up')

  def validate_username(self, username):
    user = User.query.filter_by(username=username.data).first()
    if user:
      raise ValidationError('That username is taken. Please choose a different one')
  
  def validate_email(self, email):
    user = User.query.filter_by(email=email.data).first()
    if user:
      raise ValidationError('That email is taken. Please choose a different one')

class LoginForm(FlaskForm):
  email = StringField('Email', validators=[DataRequired(), Email()])
  password = PasswordField('Password', validators=[DataRequired()])
  remember = BooleanField('Remember Me')
  submit = SubmitField('Login')

class RecipeStepForm(Form):
  stepnumber = IntegerField('Step Number')
  steptext = StringField('Instructions', validators=[DataRequired(), Length(max=200)])
  submit = SubmitField('Add Step')

class RecipeIngredientForm(Form):
  ingredient = SelectField('Ingredient', choices=[(c.id, c.name) for c in Ingredient.query.all()])
  unit = SelectField('Unit', choices=[(c.id, c.name) for c in Unit.query.all()])
  amount = IntegerField('Amount', validators=[DataRequired()])

class RecipeForm(FlaskForm):
  recipename = StringField('Recipe Name', validators=[DataRequired(), Length(max=20)])
  recipedesc = TextAreaField('Recipe Description', validators=[DataRequired(), Length(max=100)])
  photo = FileField('image', validators=[FileAllowed(['jpg'], 'Images only!')])
  submit = SubmitField('Create Recipe')
  steps = FieldList(
        FormField(RecipeStepForm),
        min_entries=0,
        max_entries=20
  )
  ingredients = FieldList(
        FormField(RecipeIngredientForm),
        min_entries=1,
        max_entries=20
  )

class SearchRecipeForm(FlaskForm):
  recipename = StringField('Recipe Name', validators=[DataRequired(), Length(max=20)])
