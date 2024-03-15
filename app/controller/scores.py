from flask_smorest import Blueprint
from flask.views import MethodView
from flask_jwt_extended import jwt_required
from flask_cors import cross_origin
from app.schemas.scores import FantasyPointsRequestResponse
from app.schemas.util import PostResponseSuccessSchema
from app.service.scores import ScoreService
from app.utils.common_utils import fetch_user_from_jwt

blp = Blueprint('Scores', __name__, description='Scoring related endpoints')
scoring_service = ScoreService()


@blp.route('/scores')
class Score(MethodView):
    @cross_origin()
    @blp.response(201, PostResponseSuccessSchema)
    def post(self):
        return scoring_service.upsert_scores_of_players()


@blp.route('/fantasy-points')
class Points(MethodView):
    @cross_origin()
    @blp.arguments(FantasyPointsRequestResponse)
    @blp.response(201, PostResponseSuccessSchema)
    def post(self, payload: dict):
        league_id = payload.get('league_id')
        return scoring_service.calculate_fantasy_points(league_id)
