from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for
from app.forms import RecipeForm, RecipeStepForm, SearchRecipeForm, RegistrationForm, LoginForm, RecipeIngredientForm
from app import app, db, bcrypt
from app.models import Recipe, RecipeStep, User, Unit, RecipeIngredient, Ingredient
from flask_login import login_user, current_user, logout_user, login_required

@app.route("/")
def home():
    return redirect(url_for('recipes'))

@app.route("/recipes", methods=["GET", "POST"])
def recipes():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    form = RecipeForm() #Include form to create a recipe.
    if form.validate_on_submit(): #When the create form is submitted...
        recipe = Recipe(recipename=form.recipename.data, recipedesc=form.recipedesc.data, author_id=current_user.id) #Create the recipe...
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
    searchstring = request.args.get("q")
    if searchstring is not None:
        recipes = Recipe.query.filter(Recipe.recipename.contains(searchstring)).all()
        return jsonify(Recipe.serialize_list(recipes))
    recipes = Recipe.query.all()
    return render_template('recipes.html', title='Recipes', form=form, recipes=recipes)

@app.route("/editrecipe/<int:id>", methods=["GET", "POST"])
def editrecipe(id):
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    recipe = Recipe.query.get(id)
    form = RecipeForm(obj=recipe)
    if form.validate_on_submit(): # Question here: Doesn't seem to validate in all cases.
        print("valid")
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
    else:
        print("invalid")
    return render_template('editrecipe.html', title='Edit Recipe', form=form, recipe=recipe)

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

@app.route("/account")
@login_required
def account():
    return render_template('account.html')