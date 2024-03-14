from flask_smorest import Blueprint
from flask.views import MethodView
from flask_cors import cross_origin
from flask_jwt_extended import jwt_required
from app.service.prediction import PredictionService
from app.schemas.util import PostResponseSuccessSchema
from app.schemas.prediction import PredictionRequestSchema, PredictionGetSchema, PredictionGetResponse
from app.utils.common_utils import fetch_user_from_jwt

blp = Blueprint('Prediction', __name__, description='Prediction related endpoints')
prediction_service = PredictionService()


@blp.route('/prediction')
class Prediction(MethodView):
    @cross_origin()
    @jwt_required()
    @blp.arguments(PredictionRequestSchema)
    @blp.response(201, PostResponseSuccessSchema)
    def post(self, payload: dict):
        email = fetch_user_from_jwt()
        predicted_team = payload.get('predicted_team')
        league_id = payload.get('league_id')
        team_id = payload.get('team_id')

        return prediction_service.set_prediction(email, predicted_team, league_id, team_id)

    @cross_origin()
    @jwt_required()
    @blp.arguments(PredictionGetSchema, location='query')
    @blp.response(200, PredictionGetResponse)
    def get(self, query_args: dict):
        league_id = query_args.get('league_id')
        team_id = query_args.get('team_id')
        email = fetch_user_from_jwt()

        return prediction_service.get_prediction_for_current_match(email, league_id, team_id)
