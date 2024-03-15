import os
from datetime import timedelta
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_smorest import Api
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_cors import CORS
from db import db

bcrypt = Bcrypt()
cors = CORS()


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'e54641550c5b71e3640ab4c7ae015799'
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=7)
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=14)
    app.config["API_TITLE"] = "IPL Fantasy REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = '/'
    app.config['OPENAPI_SWAGGER_UI_PATH'] = '/swagger-ui'
    app.config["OPENAPI_SWAGGER_UI_URL"] = 'https://cdn.jsdelivr.net/npm/swagger-ui-dist/'
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config['CORS_HEADERS'] = 'Content-Type'

    migrate = Migrate(app, db)
    jwt = JWTManager(app)
    db.init_app(app)
    bcrypt.init_app(app)
    cors.init_app(app)
    app.app_context().push()

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

    from app.controller.players import blp as players
    from app.controller.users import blp as users
    from app.controller.teams import blp as teams
    from app.controller.leagues import blp as leagues
    from app.controller.tournaments import blp as tournaments
    from app.controller.match import blp as match
    from app.controller.ipl_teams import blp as ipl_teams
    from app.controller.global_rules import blp as global_rules
    from app.controller.prediction import blp as prediction
    from app.controller.scores import blp as scores

    api = Api(app)
    api.register_blueprint(players)
    api.register_blueprint(users)
    api.register_blueprint(teams)
    api.register_blueprint(leagues)
    api.register_blueprint(tournaments)
    api.register_blueprint(match)
    api.register_blueprint(ipl_teams)
    api.register_blueprint(global_rules)
    api.register_blueprint(prediction)
    api.register_blueprint(scores)

    return app


run_app = create_app()
