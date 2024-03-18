from flask_smorest import Blueprint
from flask.views import MethodView
from flask_jwt_extended import jwt_required
from flask_cors import cross_origin
from app.schemas.leaderboard import MatchLeaderBoardRequestSchema, MatchLeaderBoardResponseSchema
from app.service.leaderboard import LeaderBoardService
from app.utils.common_utils import fetch_user_from_jwt

blp = Blueprint('LeaderBoard', __name__, description='LeaderBoard related endpoints')
service = LeaderBoardService


@blp.route('/match-leaderboard')
class MatchLeaderboard(MethodView):
    @cross_origin()
    @jwt_required()
    @blp.arguments(MatchLeaderBoardRequestSchema, location='query')
    @blp.response(200, MatchLeaderBoardResponseSchema(many=True))
    def get(self, query_args: dict):
        match_id = query_args.get('match_id')
        league_id = query_args.get('league_id')
        email = fetch_user_from_jwt()

        return service.get_match_leader_board(match_id, league_id, email)
