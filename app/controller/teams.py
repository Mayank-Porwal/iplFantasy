from flask_smorest import Blueprint
from flask.views import MethodView
from flask_jwt_extended import jwt_required
from flask_cors import cross_origin
from app.schemas.teams import (CreateTeamSchema, GetTeamResponseSchema, TeamResponseSchema, EditTeamRequestSchema,
                               GetTeamQuerySchema)
from app.schemas.util import PostResponseSuccessSchema
from app.service.teams import TeamService
from app.utils.common_utils import fetch_user_from_jwt

blp = Blueprint('Teams', __name__, description='Team related endpoints')
team_service = TeamService()


@blp.route('/team')
class UserTeam(MethodView):
    @cross_origin()
    @jwt_required()
    @blp.arguments(GetTeamQuerySchema, location='query')
    @blp.response(200, GetTeamResponseSchema)
    def get(self, query_args: dict):
        team_id = query_args.get('team_id')
        email = fetch_user_from_jwt()

        return team_service.get_team_details(team_id, email)

    @cross_origin()
    @jwt_required()
    @blp.arguments(CreateTeamSchema)
    @blp.response(201, PostResponseSuccessSchema)
    def post(self, payload: dict):
        name = payload.get('team_name')
        email = fetch_user_from_jwt()

        return team_service.create_team(name, email)

    @cross_origin()
    @jwt_required()
    @blp.arguments(CreateTeamSchema)
    @blp.response(201, PostResponseSuccessSchema)
    def delete(self, payload: dict):
        team_name = payload.get('team_name')
        email = fetch_user_from_jwt()

        return team_service.delete_team(team_name, email)

    @cross_origin()
    @jwt_required()
    @blp.arguments(EditTeamRequestSchema)
    @blp.response(201, PostResponseSuccessSchema)
    def put(self, payload: dict):
        team_id = payload.get('team_id')
        players = payload.get('players')
        substitutions = payload.get('substitutions')
        email = fetch_user_from_jwt()

        return team_service.edit_team(team_id, email, players, substitutions)


@blp.route('/my-teams')
class MyTeams(MethodView):
    @cross_origin()
    @jwt_required()
    @blp.response(200, TeamResponseSchema(many=True))
    def get(self):
        email = fetch_user_from_jwt()
        return team_service.get_all_teams_for_user(email)
