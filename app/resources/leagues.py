from flask_smorest import Blueprint, abort
from flask.views import MethodView
from app.schemas.leagues import LeagueSchema, JoinLeagueSchema, TransferLeagueOwnershipSchema
from app.schemas.util import PostResponseSuccessSchema
from app.models.leagues import UserLeague as UserLeagueModel, LeagueInfo
from app.models.teams import UserTeam as UserTeamModel
from app.models.users import User
from util import LeagueType, generate_uuid
from db import db

blp = Blueprint('Leagues', __name__, description='League related endpoints')


@blp.route('/league')
class UserLeague(MethodView):
    @blp.arguments(LeagueSchema)
    @blp.response(201, PostResponseSuccessSchema)
    def post(self, payload):
        name = payload.get('league_name')
        email = payload.get('email')
        league_type = payload.get('type')

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
        return {'message': f'Successfully created the league. Code to join: {league.join_code}'}

    @blp.arguments(LeagueSchema)
    @blp.response(201, PostResponseSuccessSchema)
    def delete(self, payload):
        league_name = payload.get('league_name')
        email = payload.get('email')

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
    @blp.arguments(JoinLeagueSchema)
    @blp.response(201, PostResponseSuccessSchema)
    def post(self, payload):
        team_name = payload.get('team_name')
        join_code = payload.get('code')
        email = payload.get('email')
        league_type = payload.get('type')
        league_name = payload.get('league_name')

        # Checking if the league exists or not
        league = UserLeagueModel.query.filter_by(name=league_name, is_active=True).first()
        if not league:
            abort(422, message='League does not exist. Please create one to join.')

        # If the league is private, validate the join code
        if league_type == LeagueType.private.name:
            if league.join_code != join_code:
                abort(422, message='The join code is incorrect. Please try again.')

        # Checking if user has already joined the league with current team
        user = User.query.filter_by(email=email).first()
        if not user:
            abort(403, message=f'User with email: {email} does not exist')

        league_info = LeagueInfo.query.filter_by(league_id=league.id, user_id=user.id, is_active=True).first()

        # Check if the team trying to join exists or not, and the user is the owner or not
        team = UserTeamModel.query.filter_by(name=team_name, user_id=user.id, is_active=True).first()

        if team:
            if league_info:
                if league_info.team_id == team.id:
                    abort(409, message=f"You've already joined {league.name} with {team_name}.")
                else:
                    abort(409, message="You can't join with multiple teams in the same league.")

            join = LeagueInfo(league_id=league.id, user_id=user.id, team_id=team.id)
            join.save()
            return {'message': f'Successfully joined the league: {league.name} with team: {team.name}.'}

        abort(422, message='Please create a team to join the league')


@blp.route('/transfer-league-ownership')
class TransferLeagueOwnership(MethodView):
    @blp.arguments(TransferLeagueOwnershipSchema)
    @blp.response(200, PostResponseSuccessSchema)
    def put(self, payload):
        league_name = payload.get('league_name')
        email = payload.get('email')
        new_owner = payload.get('new_owner')

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
