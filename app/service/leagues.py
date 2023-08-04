from flask_smorest import abort
from app.models.leagues import UserLeague as UserLeagueModel, LeagueInfo
from app.models.users import User
from app.models.teams import UserTeam as UserTeamModel


def join_league(team_name, email, join_code=None, league_name=None):
    league = None

    if join_code:
        league = UserLeagueModel.query.filter_by(join_code=join_code, is_active=True).first()
    elif league_name:
        league = UserLeagueModel.query.filter_by(name=league_name, is_active=True).first()
    else:
        abort(400, message='Payload must contain either join_code or league_name.')

    # Checking if the league exists or not
    if not league:
        abort(422, message='League does not exist. Please create one to join.')

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
        return league.name

    abort(422, message='Please create a team to join the league')
