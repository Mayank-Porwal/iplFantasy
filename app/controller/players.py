from flask_smorest import Blueprint
from flask.views import MethodView
from flask_jwt_extended import jwt_required
from app.schemas.player import PlayerResponseSchema, PlayerByCategoryQuerySchema, PlayerByTeamQuerySchema
from app.service.players import PlayerService

blp = Blueprint('Players', __name__, description='Player related endpoints')
player_service = PlayerService()


@blp.route('/players')
class PlayersList(MethodView):
    @jwt_required()
    @blp.response(200, PlayerResponseSchema(many=True))
    def get(self):
        return player_service.get_all_players()


@blp.route('/player/<int:player_id>')
class Player(MethodView):
    @jwt_required()
    @blp.response(200, PlayerResponseSchema)
    def get(self, player_id: int):
        return player_service.get_player_by_id(player_id)


@blp.route('/player/category')
class PlayerByCategory(MethodView):
    @jwt_required()
    @blp.arguments(PlayerByCategoryQuerySchema, location='query')
    @blp.response(200, PlayerResponseSchema(many=True))
    def get(self, query_args: dict):
        category = query_args.get('category')
        return player_service.get_all_players_by_category(category)


@blp.route('/player/team')
class PlayerByIplTeam(MethodView):
    @jwt_required()
    @blp.arguments(PlayerByTeamQuerySchema, location='query')
    @blp.response(200, PlayerResponseSchema(many=True))
    def get(self, query_args: dict):
        team = query_args.get('team')
        return player_service.get_all_players_by_team(team)
