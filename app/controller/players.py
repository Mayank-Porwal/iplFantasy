from flask_smorest import Blueprint
from flask.views import MethodView
from flask_jwt_extended import jwt_required
from flask_cors import cross_origin
from app.schemas.player import PlayerResponseSchema, PlayerByCategoryQuerySchema, PlayerByTeamQuerySchema
from app.schemas.util import PostResponseSuccessSchema
from app.service.players import PlayerService

blp = Blueprint('Players', __name__, description='Player related endpoints')
player_service = PlayerService()


@blp.route('/players')
class PlayersList(MethodView):
    @cross_origin()
    @jwt_required()
    @blp.response(200, PlayerResponseSchema(many=True))
    def get(self):
        return player_service.get_all_players()

    @cross_origin()
    @blp.response(201, PostResponseSuccessSchema)
    def post(self):
        """
        This endpoint will populate the player table with all the IPL players before the tournament starts.

        :param payload: A dict
        :return: A success or an error code
        """
        return player_service.save_all_players()


@blp.route('/player/<int:player_id>')
class Player(MethodView):
    @cross_origin()
    @jwt_required()
    @blp.response(200, PlayerResponseSchema)
    def get(self, player_id: int):
        return player_service.get_player_by_id(player_id)


@blp.route('/player/category')
class PlayerByCategory(MethodView):
    @cross_origin()
    @jwt_required()
    @blp.arguments(PlayerByCategoryQuerySchema, location='query')
    @blp.response(200, PlayerResponseSchema(many=True))
    def get(self, query_args: dict):
        category = query_args.get('category')
        return player_service.get_all_players_by_category(category)


@blp.route('/player/team')
class PlayerByIplTeam(MethodView):
    @cross_origin()
    @jwt_required()
    @blp.arguments(PlayerByTeamQuerySchema, location='query')
    @blp.response(200, PlayerResponseSchema(many=True))
    def get(self, query_args: dict):
        team = query_args.get('team')
        return player_service.get_all_players_by_team(team)
