from flask_smorest import Blueprint
from flask.views import MethodView
from flask_jwt_extended import jwt_required
from flask_cors import cross_origin
from app.schemas.leagues import (CreateLeagueRequestSchema, CreateLeagueResponseSchema, JoinLeagueSchema,
                                 TransferLeagueOwnershipSchema, LeagueGetSchema, LeagueGetResponse,
                                 MyLeaguesQuerySchema, MyLeaguesPostSchema, MyLeaguesResponseSchema,
                                 DeleteLeagueRequestSchema, PublicLeaguesResponseSchema)
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
    @blp.response(200, LeagueGetResponse())
    def get(self, query_args: dict):
        league_id = query_args.get('league_id')
        email = fetch_user_from_jwt()

        return league_service.get_league_details(league_id, email)

    @cross_origin()
    @jwt_required()
    @blp.arguments(CreateLeagueRequestSchema)
    @blp.response(201, CreateLeagueResponseSchema)
    def post(self, payload: dict):
        league_name = payload.get('league_name')
        league_type = payload.get('type')
        email = fetch_user_from_jwt()
        team_name = payload.get('team_name')

        return league_service.create_league(league_name, league_type, email, team_name)

    @cross_origin()
    @jwt_required()
    @blp.arguments(DeleteLeagueRequestSchema)
    @blp.response(201, PostResponseSuccessSchema)
    def delete(self, payload: dict):
        league_id = payload.get('league_id')
        email = fetch_user_from_jwt()

        return league_service.delete_league(league_id, email)


@blp.route('/join-league')
class JoinLeague(MethodView):
    @cross_origin()
    @jwt_required()
    @blp.arguments(JoinLeagueSchema)
    @blp.response(201, CreateLeagueResponseSchema)
    def post(self, payload: dict):
        team_name = payload.get('team_name')
        join_code = payload.get('code')
        league_id = payload.get('league_id')
        email = fetch_user_from_jwt()

        return league_service.join_league(team_name, email, join_code, league_id)


@blp.route('/transfer-league-ownership')
class TransferLeagueOwnership(MethodView):
    @cross_origin()
    @jwt_required()
    @blp.arguments(TransferLeagueOwnershipSchema)
    @blp.response(200, PostResponseSuccessSchema)
    def put(self, payload: dict):
        league_id = payload.get('league_id')
        new_owner = payload.get('new_owner')
        email = fetch_user_from_jwt()

        return league_service.transfer_league_ownership(league_id, email, new_owner)


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


@blp.route('/public-leagues')
class PublicLeague(MethodView):
    @cross_origin()
    @jwt_required()
    @blp.arguments(MyLeaguesPostSchema)
    @blp.arguments(MyLeaguesQuerySchema, location='query')
    @blp.response(200, PublicLeaguesResponseSchema)
    def post(self, payload: dict, query_args: dict):
        email = fetch_user_from_jwt()
        filter_data = payload.get('filter_data')
        size = query_args.get('size')
        page = query_args.get('page')

        return league_service.get_public_leagues(email, filter_data, page, size)
