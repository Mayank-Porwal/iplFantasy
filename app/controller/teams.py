from flask_smorest import Blueprint
from flask.views import MethodView
from flask_jwt_extended import jwt_required
from app.schemas.teams import TeamSchema, GetTeamResponseSchema, TeamResponseSchema
from app.schemas.util import PostResponseSuccessSchema
from app.service.teams import TeamService
from app.utils.common_utils import fetch_user_from_jwt

blp = Blueprint('Teams', __name__, description='Team related endpoints')
team_service = TeamService()


@blp.route('/team')
class UserTeam(MethodView):
    @jwt_required()
    @blp.arguments(TeamSchema, location='query')
    @blp.response(200, GetTeamResponseSchema(many=True))
    def get(self, query_args: dict):
        team_name = query_args.get('team_name')
        email = fetch_user_from_jwt()

        return team_service.get_team_details(team_name, email)

    @jwt_required()
    @blp.arguments(TeamSchema)
    @blp.response(201, PostResponseSuccessSchema)
    def post(self, payload: dict):
        name = payload.get('team_name')
        players = payload.get('players')
        email = fetch_user_from_jwt()

        return team_service.create_team(name, players, email)

    @jwt_required()
    @blp.arguments(TeamSchema)
    @blp.response(201, PostResponseSuccessSchema)
    def delete(self, payload: dict):
        team_name = payload.get('team_name')
        email = fetch_user_from_jwt()

        return team_service.delete_team(team_name, email)


@blp.route('/my-teams')
class MyTeams(MethodView):
    @jwt_required()
    @blp.response(200, TeamResponseSchema(many=True))
    def get(self):
        email = fetch_user_from_jwt()
        return team_service.get_all_teams_for_user(email)
