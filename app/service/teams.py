from datetime import datetime
from flask_smorest import abort
from app.models.users import User
from app.models.teams import UserTeam
from app.models.snapshot import Snapshot
from app.models.match import Match
from app.dao.leagues import LeagueDAO
from app.dao.users import UserDAO
from app.dao.teams import TeamDAO
from app.dao.players import PlayerDAO
from app.dao.snapshot import SnapshotDAO
from app.dao.match import MatchDAO
from app.utils.teams import TeamUtils


class TeamService:
    def __init__(self) -> None:
        self.team_dao = TeamDAO
        self.user_dao = UserDAO
        self.league_dao = LeagueDAO
        self.player_dao = PlayerDAO
        self.snapshot_dao = SnapshotDAO
        self.match_dao = MatchDAO

    def create_team(self, team_name: str, email: str) -> dict:
        user: User = self.user_dao.get_user_by_email(email)
        if not user:
            abort(403, message=f'User with email: {email} does not exist')

        team: UserTeam = self.team_dao.get_team_by_name(team_name)
        if team:
            if team.user_id == user.id:
                abort(409, message=f'{team_name} already exists')

        self.team_dao.create_team(team_name, user.id)
        return {'message': 'Successfully created the team.'}

    def delete_team(self, team_id: int, email: str) -> dict:
        user: User = self.user_dao.get_user_by_email(email)
        if not user:
            abort(403, message=f'User with email: {email} does not exist')

        team: UserTeam = self.team_dao.get_team_by_id(team_id)
        if team:
            if team.user_id == user.id:
                league_info: list[Snapshot] = self.snapshot_dao.get_all_league_info_by_team(team.id)
                self.team_dao.delete_team(league_info, team)
                return {'message': f'{team.name} deleted successfully.'}

            abort(403, message='Team can be deleted by its owner only')
        abort(403, message='The team you are trying to delete does not exist')

    def edit_team(self, team_id: int, email: str, players: dict, substitutions: int) -> dict:
        user: User = self.user_dao.get_user_by_email(email)
        if not user:
            abort(403, message=f'User with email: {email} does not exist')

        team: UserTeam = self.team_dao.get_team_by_id(team_id)
        if not team:
            abort(403, message='The team you are trying to edit does not exist')

        if team.user_id != user.id:
            abort(403, message='Team can be edited by its owner only')

        try:
            self.team_dao.edit_team(team, players, substitutions)
            return {'message': 'Team saved successfully'}
        except Exception as e:
            abort(500, message=f'Failed with error: {e}')

    def get_team_details(self, team_id: int, email: str) -> list[dict] | dict:
        user: User = self.user_dao.get_user_by_email(email)
        if not user:
            abort(403, message=f'User with email: {email} does not exist')

        team: UserTeam = self.team_dao.get_team_by_id(team_id)
        if team:
            if team.user_id != user.id:
                abort(403, message=f"You can't view this team")
        else:
            abort(404, message='Team not found')

        match_id: int = MatchDAO.get_current_match_id_by_status().id
        league_info: Snapshot = SnapshotDAO.get_league_info_by_team_id(team_id, match_id)

        draft_team: list = TeamUtils.create_team_players_dict(team.draft_players) if team.draft_players else []
        last_submitted_team: list = TeamUtils.create_team_players_dict(league_info.team_snapshot) \
            if league_info.team_snapshot else []
        response = {
            'id': team.id,
            'name': team.name,
            'substitutions': team.draft_remaining_subs,
            'points': league_info.cumulative_points,
            'rank': league_info.rank,
            'draft_team': draft_team,
            'last_submitted_team': last_submitted_team,
            'previous_remaining_substitutes':  league_info.remaining_substitutes
        }

        return response

    def get_all_teams_for_user(self, email: str) -> list[UserTeam] | dict:
        user: User = self.user_dao.get_user_by_email(email)
        if not user:
            abort(403, message=f'User with email: {email} does not exist')

        teams = self.team_dao.get_all_user_teams(user.id)
        if not teams:
            abort(404, message='No teams created by the user yet. Create one now.')

        return teams
