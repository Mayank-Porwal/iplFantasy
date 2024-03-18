from flask_smorest import Blueprint
from flask.views import MethodView
from flask_cors import cross_origin
from app.schemas.util import PostResponseSuccessSchema
from app.service.scores import ScoreService

blp = Blueprint('Scores', __name__, description='Scoring related endpoints')
scoring_service = ScoreService()


@blp.route('/scores')
class Score(MethodView):
    @cross_origin()
    @blp.response(201, PostResponseSuccessSchema)
    def post(self):
        return scoring_service.upsert_scores_of_players()
