import pandas as pd
from flask_smorest import Blueprint, abort
from flask.views import MethodView, request
from sqlalchemy import text
from flask_jwt_extended import get_jwt, jwt_required
from app.schemas.leagues import LeagueSchema, JoinLeagueSchema, TransferLeagueOwnershipSchema, LeagueGetSchema, \
    LeagueGetResponse
from app.schemas.util import PostResponseSuccessSchema
from app.models.leagues import UserLeague as UserLeagueModel, LeagueInfo
from app.models.users import User
from app.service.leagues import join_league
from util import LeagueType, generate_uuid, fetch_user_from_jwt
from db import db, conn

blp = Blueprint('Leagues', __name__, description='League related endpoints')


@blp.route('/league')
class UserLeague(MethodView):
    @jwt_required()
    @blp.arguments(LeagueGetSchema, location='query')
    @blp.response(200, LeagueGetResponse(many=True))
    def get(self, query_args):
        league_name = query_args.get('league_name')

        query = """
        select team_rank, ut.name as team_name, u.first_name || ' ' || u.last_name as owner, substitutes, team_points
        from league_info li
        join user_league ul 
        on li.league_id = ul.id 
        join user_team ut 
        on ut.id = li.team_id
        join public."user" u 
        on u.id = ut.user_id 
        where ul."name" = :league_name
        ;
        """

        result = conn().execute(text(query), {'league_name': league_name}).fetchall()
        df = pd.DataFrame(result, columns=['rank', 'team_name', 'team_owner', 'remaining_subs', 'points'])

        return df.to_dict('records')

    @jwt_required()
    @blp.arguments(LeagueSchema)
    @blp.response(201, PostResponseSuccessSchema)
    def post(self, payload):
        name = payload.get('league_name')
        league_type = payload.get('type')
        email = fetch_user_from_jwt()
        team_name = request.args.get('team_name')

        owner = User.query.filter_by(email=email).first()
        if not owner:
            abort(403, message=f'User with email: {email} does not exist')

        if UserLeagueModel.query.filter_by(name=name, owner=int(owner.id), is_active=True).first():
            abort(409, message=f'{name} already exists')

        if league_type == LeagueType.private.name:
            league = UserLeagueModel(name=name, owner=int(owner.id), league_type=league_type, join_code=generate_uuid())
        else:
            league = UserLeagueModel(name=name, owner=int(owner.id), league_type=league_type)

        league.save()
        if team_name:
            joined_league = join_league(team_name, email, league.join_code, name)
            return {'message': f'Successfully created the league {joined_league} and joined with team {team_name}'}

        if league.join_code:
            return {'message': f'Successfully created the {league_type} league. Code to join: {league.join_code}'}

        return {'message': f'Successfully created the {league_type} league.'}

    @jwt_required()
    @blp.arguments(LeagueSchema)
    @blp.response(201, PostResponseSuccessSchema)
    def delete(self, payload):
        league_name = payload.get('league_name')
        email = fetch_user_from_jwt()

        league = UserLeagueModel.query.filter_by(name=league_name, is_active=True).first()
        if league:
            owner = User.query.filter_by(email=email).first()
            if not owner:
                abort(403, message=f'User with email: {email} does not exist')
            if league.owner == int(owner.id):
                league_info = LeagueInfo.query.filter_by(league_id=league.id).all()
                for row in league_info:
                    row.is_active = False

                league.is_active = False
                db.session.commit()

                return {'message': f'{league_name} deleted successfully.'}
            abort(403, message='League can be deleted by its owner only')
        abort(403, message='The league you are trying to delete does not exist')


@blp.route('/join-league')
class JoinLeague(MethodView):
    @jwt_required()
    @blp.arguments(JoinLeagueSchema)
    @blp.response(201, PostResponseSuccessSchema)
    def post(self, payload):
        team_name = payload.get('team_name')
        join_code = payload.get('code')
        league_name = payload.get('league_name')
        email = fetch_user_from_jwt()

        league = join_league(team_name, email, join_code, league_name)
        return {'message': f'Successfully joined the league: {league.name} with team: {team_name}.'}


@blp.route('/transfer-league-ownership')
class TransferLeagueOwnership(MethodView):
    @jwt_required()
    @blp.arguments(TransferLeagueOwnershipSchema)
    @blp.response(200, PostResponseSuccessSchema)
    def put(self, payload):
        league_name = payload.get('league_name')
        new_owner = payload.get('new_owner')
        email = fetch_user_from_jwt()

        league = UserLeagueModel.query.filter_by(name=league_name, is_active=True).first()
        if league:
            owner = User.query.filter_by(email=email).first()
            if league.owner == int(owner.id):
                new_owner_obj = User.query.filter_by(username=new_owner).first()
                if not new_owner_obj:
                    abort(403, message=f'User {new_owner} does not exist.')

                league.owner = int(new_owner_obj.id)
                db.session.commit()
                return {'message': f'New owner of {league_name} is now: {new_owner}.'}
            abort(403, message=f"League's ownership can be modified by its owner only.")

        abort(403, message=f'The league you are trying to access does not exist.')
