from flask_smorest import Blueprint
from flask.views import MethodView
from flask_cors import cross_origin
from app.schemas.tournaments import CreateTournamentRequestSchema
from app.schemas.util import PostResponseSuccessSchema
from app.service.tournaments import TournamentService

blp = Blueprint('Tournaments', __name__, description='Tournament related endpoints')
tournament_service = TournamentService()


@blp.route('/tournament')
class Tournament(MethodView):
    @cross_origin()
    @blp.arguments(CreateTournamentRequestSchema)
    @blp.response(201, PostResponseSuccessSchema)
    def post(self, payload: dict):
        return tournament_service.create_tournament(payload)
