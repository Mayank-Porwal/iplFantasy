from flask import Blueprint, request
from app import db
from app.models import UserTeam, User, LeagueInfo, Player
from app.teams.utils import get_team_object
from app.players.utils import get_player_object

teams = Blueprint('teams', __name__)


@teams.route('/user-team')
def get_team():
    team_name = request.args.get('name')
    user_name = request.args.get('user_name')

    if not team_name:
        return {'message': 'team_name missing in args'}, 500
    if not user_name:
        return {'message': 'user_name missing in args'}, 500

    user = User.query.filter_by(username=user_name).first()
    if not user:
        return {'message': f'{user_name} does not exist'}, 403

    team = UserTeam.query.filter_by(name=team_name, user_id=user.id).first()
    if not team:
        return {'message': 'Team not found.'}, 404

    player_ids = [player['id'] for player in team.players]
    players_list = Player.query.filter(Player.id.in_(player_ids)).all()
    if players_list:
        return [get_player_object(player) for player in players_list], 200
    return {'message': 'Invalid players.'}, 404


@teams.route('/my-teams')
def get_my_teams():
    user_name = request.args.get('user_name')

    if not user_name:
        return {'message': 'user_name missing in args'}, 500

    user = User.query.filter_by(username=user_name).first()
    if not user:
        return {'message': f'{user_name} does not exist'}, 403

    team_list = UserTeam.query.filter_by(user_id=user.id).all()
    if team_list:
        return [get_team_object(team) for team in team_list], 200

    return {'message': 'No teams created by user yet.'}, 404


@teams.route('/create-team', methods=['POST'])
def create_team():
    payload = request.get_json()
    name = payload.get('name')
    players = payload.get('players')
    user_name = payload.get('user_name')

    user = User.query.filter_by(username=user_name).first()
    if not user:
        return {'message': f'{user_name} does not exist'}, 403

    if UserTeam.query.filter_by(name=name, user_id=user.id).first():
        return {'message': f'{name} already exists'}, 409

    team = UserTeam(name=name, players=players, user_id=user.id)
    team.save()
    return {'message': 'Successfully created the team.'}, 201


@teams.route('/delete-team', methods=['POST'])
def delete_team():
    payload = request.get_json()
    team_name = payload.get('team_name')
    user_name = payload.get('user_name')

    user = User.query.filter_by(username=user_name).first()
    if not user:
        return {'message': f'{user_name} does not exist'}, 403

    team = UserTeam.query.filter_by(name=team_name).first()
    if team:
        if team.user_id == user.id:
            LeagueInfo.query.filter_by(team_id=team.id).delete()
            UserTeam.query.filter_by(id=team.id).delete()
            db.session.commit()
            return {'message': f'{team_name} deleted successfully.'}, 201
        return {'message': f'Team can be deleted by its owner only.'}, 403
    return {'message': f'The team you are trying to delete does not exist.'}, 403
