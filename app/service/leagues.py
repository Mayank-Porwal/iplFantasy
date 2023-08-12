import pandas as pd
from flask_smorest import abort
from app.models.leagues import UserLeague, LeagueInfo
from app.models.users import User
from app.models.teams import UserTeam
from app.dao.leagues import LeagueDAO
from app.dao.users import UserDAO
from app.dao.teams import TeamDAO
from app.utils.leagues import LeagueType


class LeagueService:
    def __init__(self) -> None:
        self.league_dao = LeagueDAO
        self.user_dao = UserDAO
        self.team_dao = TeamDAO

    def create_league(self, league_name: str, league_type: str, email: str, team_name: str = None) -> dict:
        owner: User = self.user_dao.get_user_by_email(email)
        if not owner:
            abort(403, message=f'User with email: {email} does not exist')

        league: UserLeague = self.league_dao.get_league_by_name(league_name)
        if league:
            if league.owner == int(owner.id):
                abort(409, message=f'{league_name} already exists')

        if league_type == LeagueType.private.name:
            league = self.league_dao.create_league(league_name, league_type, owner.id, True)
        else:
            league = self.league_dao.create_league(league_name, league_type, owner.id, False)

        if team_name:
            if league_type == LeagueType.private.name:
                return self.join_league(team_name, email, league.join_code, league_name)
            return self.join_league(team_name, email, None, league_name)

        if league.join_code:
            return {'message': f'Successfully created the {league_type} league. Code to join: {league.join_code}.'}

        return {'message': f'Successfully created the {league_type} league.'}

    def join_league(self, team_name: str, email: str, join_code: str = None, league_name: str = None) -> dict[str, str]:
        league: UserLeague = UserLeague()

        if join_code:
            league = LeagueDAO.get_league_by_code(join_code)
        elif league_name:
            league = LeagueDAO.get_league_by_name(league_name)
        else:
            abort(400, message='Payload must contain either join_code or league_name.')

        # Checking if the league exists or not
        if not league:
            abort(422, message='League does not exist. Please create one to join.')

        # Checking if user has already joined the league with current team
        user: User = self.user_dao.get_user_by_email(email)
        if not user:
            abort(403, message=f'User with email: {email} does not exist')

        league_info = LeagueDAO.get_league_info_by_user(league.id, user.id)

        # Check if the team trying to join exists or not, and the user is the owner or not
        team: UserTeam = self.team_dao.get_team_by_name(team_name)

        if team:
            if team.user_id == user.id:
                if league_info:
                    if league_info.team_id == team.id:
                        abort(409, message=f"You've already joined {league.name} with {team_name}.")
                    else:
                        abort(409, message="You can't join with multiple teams in the same league.")

                LeagueDAO.join_league(league.id, user.id, team.id)
                return {'message': f'Successfully joined the league: {league.name} with team: {team_name}.'}

            abort(403, message=f'You are not the owner of the team: {team_name} ')
        abort(422, message='Please create a team to join the league')

    def delete_league(self, league_name: str, email: str) -> dict:
        league: UserLeague = self.league_dao.get_league_by_name(league_name)

        if league:
            owner = self.user_dao.get_user_by_email(email)
            if not owner:
                abort(403, message=f'User with email: {email} does not exist')
            if league.owner == int(owner.id):
                league_info: list[LeagueInfo] = self.league_dao.get_all_league_info_by_league(league.id)
                self.league_dao.delete_league(league_info, league)
                return {'message': f'{league_name} deleted successfully.'}
            abort(403, message='League can be deleted by its owner only')
        abort(403, message='The league you are trying to delete does not exist')

    def get_league_details(self, league_name: str, email: str) -> list[dict]:
        user: User = self.user_dao.get_user_by_email(email)
        league: UserLeague = self.league_dao.get_league_by_name(league_name)

        league_info: LeagueInfo = self.league_dao.get_league_info_by_user(league.id, user.id)
        if league_info or league.league_type == LeagueType.public.name:
            result = self.league_dao.get_league_details(league_name)
            df = pd.DataFrame(result, columns=['rank', 'team_name', 'team_owner', 'remaining_subs', 'points'])
            return df.to_dict('records')
        abort(403, message='Join the league to view the details.')

    def transfer_league_ownership(self, league_name: str, owner_email: str, new_owner_email: str) -> dict:
        league: UserLeague = self.league_dao.get_league_by_name(league_name)

        if league:
            owner = self.user_dao.get_user_by_email(owner_email)
            if league.owner == int(owner.id):
                new_owner = self.user_dao.get_user_by_email(new_owner_email)
                if not new_owner:
                    abort(403, message=f'User {new_owner_email} does not exist.')

                self.league_dao.transfer_league_ownership(league, new_owner.id)
                return {'message': f'New owner of {league_name} is now: {new_owner}.'}

            abort(403, message=f"League's ownership can be modified by its owner only.")
        abort(403, message=f'The league you are trying to access does not exist.')

    def get_my_leagues(self, email: str, search_obj: list[dict], page: int, size: int) -> dict:
        user: User = self.user_dao.get_user_by_email(email)
        if not user:
            abort(403, message=f'User with email: {email} does not exist')

        paginated_results = self.league_dao.get_paginated_my_leagues(user.id, search_obj, page, size)

        data = []

        if len(paginated_results.items) > 0:
            for row in paginated_results.items:
                li, ul, ut, u = row
                data.append(
                    {
                        'active': ul.is_active,
                        'league_name': ul.name,
                        'type': ul.league_type,
                        'team': ut.name,
                        'rank': li.team_rank,
                        'owner': ul.owner == user.id
                    }
                )

        return {
            "data": data,
            "total": paginated_results.total,
            "total_pages": paginated_results.pages,
            "page": paginated_results.page,
            "size": paginated_results.per_page
        }
