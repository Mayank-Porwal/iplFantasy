from flask_smorest import Blueprint, abort
from flask.views import MethodView
from app.schemas.player import PlayerResponseSchema, PlayerByCategoryQuerySchema, PlayerByTeamQuerySchema
from app.models.player import Player as PlayerModel

blp = Blueprint('Players', __name__, description='Player related endpoints')


@blp.route('/players')
class PlayersList(MethodView):
    @blp.response(200, PlayerResponseSchema(many=True))
    def get(self):
        return PlayerModel.query.all()


@blp.route('/player/<int:player_id>')
class Player(MethodView):
    @blp.response(200, PlayerResponseSchema)
    def get(self, player_id):
        return PlayerModel.query.get_or_404(player_id)


@blp.route('/player/category')
class PlayerByCategory(MethodView):
    @blp.arguments(PlayerByCategoryQuerySchema, location='query')
    @blp.response(200, PlayerResponseSchema(many=True))
    def get(self, query_args):
        category = query_args.get('category')
        players_list = PlayerModel.query.filter_by(category=category.lower()).all()
        if players_list:
            return players_list
        abort(404, message='Invalid category.')


@blp.route('/player/team')
class PlayerByIplTeam(MethodView):
    @blp.arguments(PlayerByTeamQuerySchema, location='query')
    @blp.response(200, PlayerResponseSchema(many=True))
    def get(self, query_args):
        team = query_args.get('team')
        players_list = PlayerModel.query.filter_by(ipl_team=team.upper()).all()
        if players_list:
            return players_list
        abort(404, message='Invalid team.')
