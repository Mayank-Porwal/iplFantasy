from flask_smorest import Blueprint
from flask.views import MethodView
from flask_cors import cross_origin
from flask_jwt_extended import jwt_required
from app.schemas.util import PostResponseSuccessSchema
from app.schemas.scores import LastFiveMatchesStatsRequestSchema, LastFiveMatchesStatsResponseSchema
from app.service.scores import ScoreService

blp = Blueprint('Scores', __name__, description='Scoring related endpoints')
service = ScoreService()


@blp.route('/scores')
class Score(MethodView):
    @cross_origin()
    @blp.response(201, PostResponseSuccessSchema)
    def post(self):
        return service.upsert_scores_of_players()


@blp.route('/last-n-matches-stats')
class LastFiveMatchesStats(MethodView):
    @cross_origin()
    @jwt_required()
    @blp.arguments(LastFiveMatchesStatsRequestSchema, location='query')
    @blp.response(200, LastFiveMatchesStatsResponseSchema(many=True))
    def get(self, query_args: dict):
        player_id = query_args.get('player_id')
        n = query_args.get('n')
        return service.get_last_n_stats_for_a_player(player_id, n)
