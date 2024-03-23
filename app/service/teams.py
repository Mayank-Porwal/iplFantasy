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
        if team:
            if team.user_id == user.id:
                match: Match = self.match_dao.get_current_match_id_by_status()
                league_info: Snapshot = self.snapshot_dao.get_league_info_by_team_id(team.id, match.id)

                if league_info:
                    self.team_dao.edit_team(team, players)
                    self.snapshot_dao.set_substitutions(substitutions, league_info)
                    return {'message': f'{team.name} saved successfully.'}
                abort(404, message='No association of team found')

            abort(403, message='Team can be edited by its owner only')
        abort(403, message='The team you are trying to edit does not exist')

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

        snapshot: Snapshot = SnapshotDAO.get_latest_row_for_team(team_id)
        # match_id: int = MatchDAO.get_current_match_id_by_status().id
        # league_info: Snapshot = SnapshotDAO.get_league_info_by_team_id(team_id, match_id)
        # user_league_info: Snapshot = SnapshotDAO.get_league_info_for_user(league_info.league_id, user.id, match_id)
        # is_member: bool = False

        # if team:
        #     if team.user_id != user.id:
        #         if not user_league_info:
        #             abort(403, message=f"You can't view this team")
        #         is_member = True
        # else:
        #     abort(404, message='Team not found')

        last_submitted_team = []
        remaining_substitutes = 250
        cumulative_points = 0.0
        rank = -1

        if snapshot:
            last_submitted_team = snapshot.team_snapshot
            remaining_substitutes = snapshot.remaining_substitutes
            cumulative_points = snapshot.cumulative_points
            rank = snapshot.rank

        # if is_member:
        #     draft_team: list = last_submitted_team
        # else:
        #     draft_team: list = TeamUtils.create_team_players_dict(team.draft_players) if team.draft_players else []

        draft_team: list = TeamUtils.create_team_players_dict(team.draft_players) if team.draft_players else []
        response = {
            'id': team.id,
            'name': team.name,
            'substitutions': remaining_substitutes,
            'points': cumulative_points,
            'rank': rank,
            'draft_team': draft_team,
            'last_submitted_team': last_submitted_team
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
