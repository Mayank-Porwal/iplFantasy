from flask import Blueprint, request
from app.models import Player
from app.players.utils import get_player_object

players = Blueprint('players', __name__)


@players.route('/player')
def get_player():
    player_id = request.args.get('player_id')
    if not player_id:
        return {'message': 'player_id missing in args'}, 500
    player = Player.query.get(int(player_id))
    return get_player_object(player) if player else {'message': 'Player not found.'}, 404


@players.route('/players/category')
def get_players_by_category():
    category = request.args.get('category')
    players_list = Player.query.filter_by(category=category.lower()).all()
    if players_list:
        return [get_player_object(player) for player in players_list]
    return {'message': 'Invalid category.'}, 404


@players.route('/players/team')
def get_players_by_team():
    team = request.args.get('team')
    players_list = Player.query.filter_by(ipl_team=team.upper()).all()
    if players_list:
        return [get_player_object(player) for player in players_list]
    return {'message': 'Invalid team.'}, 404


@players.route('/players')
def get_all_players():
    players_list = Player.query.all()
    if players_list:
        return [get_player_object(player) for player in players_list]
    return {'message': 'Something went wrong.'}, 500
