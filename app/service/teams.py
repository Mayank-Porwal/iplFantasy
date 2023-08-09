import pandas as pd
from flask_smorest import abort
from app.models.users import User
from app.models.teams import UserTeam
from app.dao.leagues import LeagueDAO
from app.dao.users import UserDAO
from app.dao.teams import TeamDAO
from app.dao.players import PlayerDAO
from app.utils.teams import get_player_object


class TeamService:
    def __init__(self) -> None:
        self.team_dao = TeamDAO
        self.user_dao = UserDAO
        self.league_dao = LeagueDAO
        self.player_dao = PlayerDAO

    def create_team(self, team_name: str, players: dict, email: str) -> dict:
        user: User = self.user_dao.get_user_by_email(email)
        if not user:
            abort(403, message=f'User with email: {email} does not exist')

        team: UserTeam = self.team_dao.get_team_by_name(team_name)
        if team:
            if team.user_id == user.id:
                abort(409, message=f'{team_name} already exists')

        self.team_dao.create_team(team_name, players, user.id)
        return {'message': 'Successfully created the team.'}

    def delete_team(self, team_name: str, email: str) -> dict:
        user: User = self.user_dao.get_user_by_email(email)
        if not user:
            abort(403, message=f'User with email: {email} does not exist')

        team: UserTeam = self.team_dao.get_team_by_name(team_name)
        if team:
            if team.user_id == user.id:
                league_info: list = self.league_dao.get_all_league_info_by_team(team.id)
                self.team_dao.delete_team(league_info, team)
                return {'message': f'{team_name} deleted successfully.'}

            abort(403, message='Team can be deleted by its owner only')
        abort(403, message='The team you are trying to delete does not exist')

    def get_team_details(self, team_name: str, email: str) -> list[dict] | dict:
        user: User = self.user_dao.get_user_by_email(email)
        if not user:
            abort(403, message=f'User with email: {email} does not exist')

        team: UserTeam = self.team_dao.get_team_by_name(team_name)
        if team:
            if team.user_id != user.id:
                abort(403, message=f'You are not the owner of team: {team_name}.')
        else:
            abort(404, message='Team not found.')

        player_ids = [player['id'] for player in team.players]
        players_list = self.player_dao.get_list_of_players(player_ids)
        if players_list:
            players_df = pd.DataFrame([get_player_object(player) for player in players_list])
            team_df = pd.DataFrame(team.players)
            final_df = players_df.merge(team_df, on='id')
            return final_df.to_dict('records')

        abort(404, message='No players found in the team.')

    def get_all_teams_for_user(self, email: str) -> list[UserTeam] | dict:
        user: User = self.user_dao.get_user_by_email(email)
        if not user:
            abort(403, message=f'User with email: {email} does not exist')

        teams = self.team_dao.get_all_user_teams(user.id)
        if not teams:
            abort(404, message='No teams created by the user yet. Create one now.')

        return teams
