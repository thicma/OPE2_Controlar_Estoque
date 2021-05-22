from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from datetime import timedelta

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///estoque.db'
app.config['SECRET_KEY'] = 'd1e8ab4c46d1d1d40c592ef2'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=1)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login_page"
login_manager.login_message = "Para acessar esta página você precisa estar logado!"
login_manager.login_message_category = "info"

from estoque import routes


