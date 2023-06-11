import os
from flask import Flask, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate
from flasgger import Swagger

app = Flask(__name__)
app.config['SECRET_KEY'] = 'e54641550c5b71e3640ab4c7ae015799'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']

db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
swagger = Swagger(app, template_file='swagger_docs.yaml')
login_manager = LoginManager(app)
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'

from app.users.routes import users
from app.leagues.routes import leagues
from app.teams.routes import teams
from app.main.routes import main
from app.players.routes import players

app.register_blueprint(users)
app.register_blueprint(leagues)
app.register_blueprint(teams)
app.register_blueprint(main)
app.register_blueprint(players)
