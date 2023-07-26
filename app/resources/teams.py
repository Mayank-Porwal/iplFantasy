import pandas as pd
from flask_smorest import Blueprint, abort
from flask.views import MethodView
from app.schemas.teams import TeamSchema, GetTeamResponseSchema, MyTeamsRequestSchema, TeamResponseSchema
from app.schemas.util import PostResponseSuccessSchema
from app.models.teams import UserTeam as UserTeamModel
from app.models.users import User
from app.models.player import Player
from app.models.leagues import LeagueInfo
from util import get_player_object
from db import db

blp = Blueprint('Teams', __name__, description='Team related endpoints')


@blp.route('/team')
class UserTeam(MethodView):
    @blp.arguments(TeamSchema, location='query')
    @blp.response(200, GetTeamResponseSchema(many=True))
    def get(self, query_args):
        team_name = query_args.get('team_name')
        email = query_args.get('email')

        user = User.query.filter_by(email=email).first()
        if not user:
            abort(403, message=f'User with email: {email} does not exist')

        team = UserTeamModel.query.filter_by(name=team_name, user_id=user.id, is_active=True).first()
        if not team:
            abort(404, message='Team not found.')

        player_ids = [player['id'] for player in team.players]
        players_list = Player.query.filter(Player.id.in_(player_ids)).all()
        if players_list:
            players_df = pd.DataFrame([get_player_object(player) for player in players_list])
            team_df = pd.DataFrame(team.players)
            final_df = players_df.merge(team_df, on='id')
            return final_df.to_dict('records')
        abort(404, message='No players found in the team.')

    @blp.arguments(TeamSchema)
    @blp.response(201, PostResponseSuccessSchema)
    def post(self, payload):
        name = payload.get('team_name')
        players = payload.get('players')
        email = payload.get('email')

        user = User.query.filter_by(email=email).first()
        if not user:
            abort(403, message=f'User with email: {email} does not exist')

        if UserTeamModel.query.filter_by(name=name, user_id=user.id, is_active=True).first():
            abort(409, message=f'{name} already exists')

        team = UserTeamModel(name=name, players=players, user_id=user.id)
        team.save()
        return {'message': 'Successfully created the team.'}

    @blp.arguments(TeamSchema)
    @blp.response(201, PostResponseSuccessSchema)
    def delete(self, payload):
        team_name = payload.get('team_name')
        email = payload.get('email')

        user = User.query.filter_by(email=email).first()
        if not user:
            abort(403, message=f'User with email: {email} does not exist')

        team = UserTeamModel.query.filter_by(name=team_name, is_active=True).first()
        if team:
            if team.user_id == user.id:
                league_info = LeagueInfo.query.filter_by(team_id=team.id, is_active=True).all()
                if league_info:
                    for row in league_info:
                        row.is_active = False

                team.is_active = False
                db.session.commit()

                return {'message': f'{team_name} deleted successfully.'}
            abort(403, message='Team can be deleted by its owner only')
        abort(403, message='The team you are trying to delete does not exist')


@blp.route('/my-teams')
class MyTeams(MethodView):
    @blp.arguments(MyTeamsRequestSchema, location='query')
    @blp.response(200, TeamResponseSchema(many=True))
    def get(self, query_args):
        email = query_args.get('email')

        user = User.query.filter_by(email=email).first()
        if not user:
            abort(403, message=f'User with email: {email} does not exist')

        team_list = UserTeamModel.query.filter_by(user_id=user.id, is_active=True).all()
        if team_list:
            return team_list

        abort(404, message='No teams created by the user yet. Create one now.')
