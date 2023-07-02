import os
from datetime import timedelta
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate
from flasgger import Swagger
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'e54641550c5b71e3640ab4c7ae015799'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=7)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=14)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
swagger = Swagger(app, template_file='swagger_docs.yaml')
jwt = JWTManager(app)
login_manager = LoginManager(app)


@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return {'message': "The token has expired"}, 401


@jwt.invalid_token_loader
def invalid_token_callback(error):
    return {'message': 'Signature verification failed'}, 401


@jwt.unauthorized_loader
def missing_token_callback(error):
    return {'message': 'Request does not contain an access token'}, 401


@jwt.needs_fresh_token_loader
def token_not_fresh_callback(jwt_header, jwt_payload):
    return {'message': 'Token is not fresh'}, 401


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
