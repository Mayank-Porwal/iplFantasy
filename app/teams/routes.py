from flask import Blueprint, request
from app import db
from app.models import UserTeam, User
from app.teams.utils import get_team_object

teams = Blueprint('teams', __name__)


@teams.route('/team')
def get_team():
    team_id = request.args.get('team_id')
    if not team_id:
        return {'message': 'team_id missing in args'}, 500
    team = UserTeam.query.get(int(team_id))
    return get_team_object(team) if team else {'message': 'Team not found.'}, 404


@teams.route('/teams_of_user')
def get_teams_by_a_user():
    user_id = request.args.get('user_id')
    team_list = UserTeam.query.filter_by(user_id=user_id)
    if teams:
        return [get_team_object(team) for team in team_list]
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
    db.session.add(team)
    db.session.commit()
    return {'message': 'Successfully created the team.'}, 201


