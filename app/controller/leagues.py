from flask_smorest import Blueprint
from flask.views import MethodView
from flask_jwt_extended import jwt_required
from flask_cors import cross_origin
from app.schemas.leagues import LeagueSchema, JoinLeagueSchema, TransferLeagueOwnershipSchema, LeagueGetSchema, \
    LeagueGetResponse, CreateLeagueQuerySchema, MyLeaguesQuerySchema, MyLeaguesPostSchema, MyLeaguesResponseSchema
from app.schemas.util import PostResponseSuccessSchema
from app.service.leagues import LeagueService
from app.utils.common_utils import fetch_user_from_jwt

blp = Blueprint('Leagues', __name__, description='League related endpoints')
league_service = LeagueService()


@blp.route('/league')
class UserLeague(MethodView):
    @cross_origin()
    @jwt_required()
    @blp.arguments(LeagueGetSchema, location='query')
    @blp.response(200, LeagueGetResponse(many=True))
    def get(self, query_args: dict):
        league_name = query_args.get('league_name')
        email = fetch_user_from_jwt()

        return league_service.get_league_details(league_name, email)

    @cross_origin()
    @jwt_required()
    @blp.arguments(LeagueSchema)
    @blp.arguments(CreateLeagueQuerySchema, location='query')
    @blp.response(201, PostResponseSuccessSchema)
    def post(self, payload: dict, query_args: dict):
        name = payload.get('league_name')
        league_type = payload.get('type')
        email = fetch_user_from_jwt()
        team_name = query_args.get('team_name')

        return league_service.create_league(name, league_type, email, team_name)

    @cross_origin()
    @jwt_required()
    @blp.arguments(LeagueSchema)
    @blp.response(201, PostResponseSuccessSchema)
    def delete(self, payload: dict):
        league_name = payload.get('league_name')
        email = fetch_user_from_jwt()

        return league_service.delete_league(league_name, email)


@blp.route('/join-league')
class JoinLeague(MethodView):
    @cross_origin()
    @jwt_required()
    @blp.arguments(JoinLeagueSchema)
    @blp.response(201, PostResponseSuccessSchema)
    def post(self, payload: dict):
        team_name = payload.get('team_name')
        join_code = payload.get('code')
        league_name = payload.get('league_name')
        email = fetch_user_from_jwt()

        return league_service.join_league(team_name, email, join_code, league_name)


@blp.route('/transfer-league-ownership')
class TransferLeagueOwnership(MethodView):
    @cross_origin()
    @jwt_required()
    @blp.arguments(TransferLeagueOwnershipSchema)
    @blp.response(200, PostResponseSuccessSchema)
    def put(self, payload: dict):
        league_name = payload.get('league_name')
        new_owner = payload.get('new_owner')
        email = fetch_user_from_jwt()

        return league_service.transfer_league_ownership(league_name, email, new_owner)


@blp.route('/my-leagues')
class MyLeagues(MethodView):
    @cross_origin()
    @jwt_required()
    @blp.arguments(MyLeaguesPostSchema)
    @blp.arguments(MyLeaguesQuerySchema, location='query')
    @blp.response(200, MyLeaguesResponseSchema)
    def post(self, payload: dict, query_args: dict):
        email = fetch_user_from_jwt()
        filter_data = payload.get('filter_data')
        size = query_args.get('size')
        page = query_args.get('page')

        return league_service.get_my_leagues(email, filter_data, page, size)
