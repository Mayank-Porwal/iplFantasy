import pandas as pd
from flask import Blueprint, request
from sqlalchemy import func
from app.models import UserLeague, UserTeam, LeagueInfo, User
from app import db
from app.leagues.utils import LeagueType, generate_uuid

leagues = Blueprint('leagues', __name__)


@leagues.route('/create_league', methods=['POST'])
def create_league():
    payload = request.get_json()
    name = payload.get('name')
    owner_name = payload.get('owner_name')
    league_type = payload.get('type')

    owner = User.query.filter_by(username=owner_name).first()
    if not owner:
        return {'message': f'{owner_name} does not exist'}, 403

    if UserLeague.query.filter_by(name=name, owner=int(owner.id)).first():
        return {'message': f'{name} already exists'}, 409

    if league_type == LeagueType.private.name:
        league = UserLeague(name=name, owner=int(owner.id), league_type=league_type, join_code=generate_uuid())
    else:
        league = UserLeague(name=name, owner=int(owner.id), league_type=league_type)

    db.session.add(league)
    db.session.commit()
    return {'message': f'Successfully created the league. Code to join: {league.join_code}'}, 201


@leagues.route('/join_league', methods=['POST'])
def join_league():
    payload = request.get_json()
    team_name = payload.get('team_name')
    join_code = payload.get('code')
    user_name = payload.get('user_name')
    league_type = payload.get('type')
    league_name = payload.get('league_name')

    # Checking if the league exists or not
    league = UserLeague.query.filter_by(name=league_name).first()
    if not league:
        return {'message': 'League does not exist. Please create one to join.'}, 422

    # If the league is private, validate the join code
    if league_type == LeagueType.private.name:
        if league.join_code != join_code:
            return {'message': 'The join code is incorrect. Please try again.'}, 422

    # Checking if user has already joined the league with current team
    user = User.query.filter_by(username=user_name).first()
    if not user:
        return {'message': f'{user_name} does not exist'}, 403
    league_info = LeagueInfo.query.filter_by(league_id=league.id, user_id=user.id).first()

    # Check if the team trying to join exists or not and the user is the owner or not
    team = UserTeam.query.filter_by(name=team_name, user_id=user.id).first()

    if team:
        if league_info:
            if league_info.team_id == team.id:
                return {'message': f"You've already joined {league.name} with {team_name}."}, 409
            else:
                return {'message': f"You can't join with multiple teams in the same league."}, 409

        join = LeagueInfo(league_id=league.id, user_id=user.id, team_id=team.id)
        db.session.add(join)
        db.session.commit()
        return {'message': f'Successfully joined the league: {league.name} with team: {team.name}.'}, 201
    else:
        return {'message': f'Please create a team to join the league.'}, 422


@leagues.route('/delete_league', methods=['POST'])
def delete_league():
    payload = request.get_json()
    league_name = payload.get('league_name')
    owner_name = payload.get('owner_name')

    league = UserLeague.query.filter_by(name=league_name).first()
    owner = User.query.filter_by(username=owner_name).first()

    if league:
        league_name = league.name
        if not owner:
            return {'message': f'User {owner_name} does not exist.'}, 403
        if league.owner == int(owner.id):
            LeagueInfo.query.filter_by(league_id=league.id).delete()
            UserLeague.query.filter_by(id=league.id).delete()
            db.session.commit()
            return {'message': f'{league_name} deleted successfully.'}, 201
        return {'message': f'League can be deleted by its owner only.'}, 403
    return {'message': f'The league you are trying to delete does not exist.'}, 403


@leagues.route('/transfer_league_ownership', methods=['POST'])
def transfer_league_ownership():
    payload = request.get_json()
    league_id = payload.get('league_id')
    owner = payload.get('owner')
    new_owner = payload.get('new_owner')

    league = UserLeague.query.filter_by(id=league_id).first()
    league_name = league.name

    if league:
        if league.owner == owner:
            league.owner = new_owner
            db.session.commit()
            return {'message': f'{league_name} deleted successfully.'}, 201
        return {'message': f'League can be deleted by its owner only.'}, 403
    return {'message': f'The league you are trying to delete does not exist.'}, 403


@leagues.route('/my_leagues')
def get_my_leagues():
    user_id = request.args.get('user_id')
    result = db.session.query(LeagueInfo, UserLeague, UserTeam).filter(LeagueInfo.league_id == UserLeague.id).filter(
        LeagueInfo.team_id == UserTeam.id).filter(LeagueInfo.user_id == int(user_id)).all()

    if result:
        rows = []
        for row in result:
            league_info, user_league, user_team = row
            rows.append((user_league.name, user_league.league_type.name, user_team.name, league_info.team_rank))

        grouped_result = db.session.query(func.count(UserLeague.name), UserLeague.name).join(LeagueInfo).\
            group_by(UserLeague.name).all()

        df = pd.DataFrame(rows, columns=['league_name', 'league_type', 'team_name', 'team_rank'])
        grp_df = pd.DataFrame(grouped_result, columns=['cnt', 'league_name'])
        mrg = df.merge(grp_df)

        mrg['team_rank'] = mrg['team_rank'].astype(str) + ' / ' + mrg['cnt'].astype(str)
        mrg.drop('cnt', axis=1, inplace=True)

        return mrg.to_dict('records'), 200
    return {'message': 'You are not a part of any league yet. Join one now.'}, 200


@leagues.route('/public_leagues')
def get_public_leagues():
    user_id = request.args.get('user_id')
    result = db.session.query(LeagueInfo, UserLeague, UserTeam).filter(LeagueInfo.league_id == UserLeague.id).filter(
        LeagueInfo.team_id == UserTeam.id).filter(LeagueInfo.user_id == int(user_id)).all()

    if result:
        rows = []
        for row in result:
            league_info, user_league, user_team = row
            rows.append((user_league.name, user_league.league_type.name, user_team.name, league_info.team_rank))

        grouped_result = db.session.query(func.count(UserLeague.name), UserLeague.name).join(LeagueInfo).\
            group_by(UserLeague.name).all()

        df = pd.DataFrame(rows, columns=['league_name', 'league_type', 'team_name', 'team_rank'])
        grp_df = pd.DataFrame(grouped_result, columns=['cnt', 'league_name'])
        mrg = df.merge(grp_df)

        mrg['team_rank'] = mrg['team_rank'].astype(str) + ' / ' + mrg['cnt'].astype(str)
        mrg.drop('cnt', axis=1, inplace=True)

        return mrg.to_dict('records'), 200
    return {'message': 'You are not a part of any league yet. Join one now.'}, 200

