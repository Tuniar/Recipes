import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


# Configure application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'abcdef'
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['WTF_CSRF_ENABLED'] = True
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///mealmate.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'


from app import routes