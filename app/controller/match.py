from flask_smorest import Blueprint
from flask.views import MethodView
from flask_cors import cross_origin
from app.service.match import MatchService
from app.schemas.util import RequestSchemaWithTournament, PostResponseSuccessSchema

blp = Blueprint('Match', __name__, description='Match related endpoints')
match_service = MatchService()


@blp.route('/match')
class Match(MethodView):
    @cross_origin()
    @blp.arguments(RequestSchemaWithTournament)
    @blp.response(201, PostResponseSuccessSchema)
    def post(self, payload: dict):
        """
        This endpoint will populate the match table with all the fixtures before the tournament starts.

        :param payload: A dict
        :return: A success or an error code
        """
        tournament_id = payload.get('tournament_id')
        return match_service.create_all_fixtures(tournament_id, '2023-03-03', '2023-05-31')
