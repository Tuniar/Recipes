import os
import secrets
from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for
from app.forms import RecipeForm, SearchRecipeForm, RegistrationForm, LoginForm, UpdateAccountForm
from app import app, db, bcrypt
from app.models import Recipe, RecipeStep, User, Unit, RecipeIngredient, Ingredient
from flask_login import login_user, current_user, logout_user, login_required
from PIL import Image

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/images', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

@app.route("/")
def home():
    return redirect(url_for('recipes'))

@app.route("/recipes", methods=["GET", "POST"])
def recipes():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    form = RecipeForm() #Include form to create a recipe.
    sform = SearchRecipeForm()
    if form.validate_on_submit(): #When the create form is submitted...
        recipe = Recipe(recipename=form.recipename.data, recipedesc=form.recipedesc.data, author_id=current_user.id) #Create the recipe...
        if form.picture.data: #If picture exists, save it and add filename to recipe
            picture_file = save_picture(form.picture.data)
            recipe.image_file = picture_file
        db.session.add(recipe)
        db.session.commit()
        stepcount = RecipeStep.query.filter(RecipeStep.recipe_id == recipe.id).count()
        for step in form.steps.data: #Create each step in the recipe...
            stepcount += 1
            new_step = RecipeStep(stepnumber=stepcount, steptext=step['steptext'], recipe_id=recipe.id)
            db.session.add(new_step)
            db.session.commit()
        for ingredient in form.ingredients.data: #Create each ingredient in the recipe...
            ingredient = RecipeIngredient(recipe_id=recipe.id, ingredient_id=ingredient['ingredient'], unit_id=ingredient['unit'], amount=ingredient['amount'])
            db.session.add(ingredient)
            db.session.commit()
        flash('Your recipe has been created!', 'success')
        return render_template('recipes.html', title='Recipes', form=form, recipe=recipe)
    recipes = Recipe.query.all()
    return render_template('recipes.html', title='Recipes', form=form, recipes=recipes, sform=sform)

@app.route("/editrecipe/<int:id>", methods=["GET", "POST"])
def editrecipe(id):
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    recipe = Recipe.query.get(id)
    form = RecipeForm(obj=recipe)
    if form.validate_on_submit(): # Question here: Doesn't seem to validate in all cases.
        if form.picture.data: #If picture exists, save it and add filename to recipe
            picture_file = save_picture(form.picture.data)
            recipe.image_file = picture_file
        recipe.recipename = form.recipename.data
        recipe.recipedesc = form.recipedesc.data
        RecipeStep.query.filter(RecipeStep.recipe_id == recipe.id).delete()
        RecipeIngredient.query.filter(RecipeIngredient.recipe_id == recipe.id).delete()
        stepcount = RecipeStep.query.filter(RecipeStep.recipe_id == recipe.id).count()
        for step in form.steps.data: #Create each step in the recipe...
            stepcount += 1
            new_step = RecipeStep(stepnumber=stepcount, steptext=step['steptext'], recipe_id=recipe.id)
            db.session.add(new_step)
            db.session.commit()
        for ingredient in form.ingredients.data: #Create each ingredient in the recipe..
            ingredient = RecipeIngredient(recipe_id=recipe.id, ingredient_id=ingredient['ingredient'], unit_id=ingredient['unit'], amount=ingredient['amount'])
            db.session.add(ingredient)
            db.session.commit()
        flash('Your recipe has been updated!', 'success')
        return render_template('recipes.html', title='Recipes', form=form, recipe=recipe)
    return render_template('editrecipe.html', title='Edit Recipe', form=form, recipe=recipe)

@app.route("/searchrecipes", methods=["POST"]) ## Get this working and move onto style?
def searchrecipes():
    form = RecipeForm()
    sform = SearchRecipeForm()
    if form.validate_on_submit:
        if sform.ingredients.data and sform.recipename.data:
            recipes = Recipe.query.filter
            pass
        elif form.recipename.data:
            recipes = Recipe.query.filter(Recipe.recipename.like(sform.recipename.data))

        return render_template('recipes.html', title='Recipes', form=form, sform=sform, recipes=recipes)



@app.route("/deleterecipe/<int:id>", methods=["GET", "POST"])
def deleterecipe(id):
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    db.session.query(RecipeIngredient).filter(RecipeIngredient.recipe_id == id).delete()
    db.session.query(RecipeStep).filter(RecipeStep.recipe_id == id).delete()
    db.session.query(Recipe).filter(Recipe.id == id).delete()
    db.session.commit()
    return redirect(url_for('recipes'))


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('recipes'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data.lower(), password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('recipes'))
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccesful')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='images/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)
