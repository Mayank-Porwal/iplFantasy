from flask_smorest import Blueprint
from flask.views import MethodView
from flask_cors import cross_origin
from flask_jwt_extended import jwt_required
from app.service.match import MatchService
from app.schemas.util import RequestSchemaWithTournament, PostResponseSuccessSchema
from app.schemas.player import PlayingElevenResponseSchema
from app.schemas.match import CompletedMatchesResponseSchema, MarkMatchCompleteRequestSchema

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
        return match_service.create_all_fixtures(tournament_id)


@blp.route('/current-match')
class CurrentMatchPlayers(MethodView):
    @cross_origin()
    @jwt_required()
    @blp.response(200, PlayingElevenResponseSchema(many=True))
    def get(self):
        return match_service.get_lineup_for_a_match()


@blp.route('/completed-matches')
class CompletedMatches(MethodView):
    @cross_origin()
    @jwt_required()
    @blp.response(200, CompletedMatchesResponseSchema(many=True))
    def get(self):
        return match_service.get_previous_completed_matches()


@blp.route('/mark-match-complete')
class Match(MethodView):
    @cross_origin()
    @blp.arguments(MarkMatchCompleteRequestSchema)
    @blp.response(201, PostResponseSuccessSchema)
    def post(self, payload: dict):
        tournament_id = payload.get('tournament_id')
        match_id = payload.get('match_id')
        return match_service.mark_match_completed(tournament_id, match_id)


@blp.route('/mark-match-in-progress')
class Match(MethodView):
    @cross_origin()
    @blp.arguments(MarkMatchCompleteRequestSchema)
    @blp.response(201, PostResponseSuccessSchema)
    def post(self, payload: dict):
        tournament_id = payload.get('tournament_id')
        match_id = payload.get('match_id')
        return match_service.mark_match_in_progress(tournament_id, match_id)
