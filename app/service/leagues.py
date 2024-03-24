from flask_smorest import abort

import pandas as pd

from app.models.leagues import League
from app.models.scores import Scores
from app.models.users import User
from app.models.teams import UserTeam
from app.models.snapshot import Snapshot
from app.models.tournament import Tournament
from app.models.match import Match
from app.dao.leagues import LeagueDAO
from app.dao.users import UserDAO
from app.dao.teams import TeamDAO
from app.dao.snapshot import SnapshotDAO
from app.dao.prediction import PredictionDAO
from app.dao.scores import ScoresDAO
from app.dao.match import MatchDAO
from app.dao.tournaments import TournamentDAO
from app.dao.rules import LeagueRulesDAO, GlobalRulesDAO
from app.dao.fantasy_points import FantasyPointsDAO
from app.utils.leagues import LeagueType


class LeagueService:
    def __init__(self) -> None:
        self.league_dao = LeagueDAO
        self.user_dao = UserDAO
        self.team_dao = TeamDAO
        self.snapshot_dao = SnapshotDAO
        self.match_dao = MatchDAO
        self.league_rules_dao = LeagueRulesDAO

    def create_league(self, league_name: str, league_type: str, email: str, team_name: str) -> dict:
        tournament: Tournament = TournamentDAO.get_tournament()
        if not tournament:
            abort(403, message='tournament_id not found')

        owner: User = self.user_dao.get_user_by_email(email)
        if not owner:
            abort(403, message=f'User with email: {email} does not exist')

        league: League = self.league_dao.get_league_by_name(league_name)
        if league:
            if league.owner == int(owner.id):
                abort(409, message=f'{league_name} already exists')

        if league_type == LeagueType.private.name:
            league = self.league_dao.create_league(tournament.id, league_name, league_type, owner.id, True)
            joined_league = self.join_league(team_name, email, league.join_code, league.id)
        else:
            league = self.league_dao.create_league(tournament.id, league_name, league_type, owner.id, False)
            joined_league = self.join_league(team_name, email, league.join_code, league.id)

        # Create default rules for this league
        self.league_rules_dao.create_league_rules(league.id)

        return {
            'message': f'Successfully created the {league_type} league.',
            'league_id': league.id,
            'team_id': joined_league['team_id'],
            'team_name': team_name
        }

    def join_league(self, team_name: str, email: str, join_code: str = None, league_id: int = None) -> dict[str, str]:
        if join_code:
            league = LeagueDAO.get_league_by_code(join_code)
        elif league_id:
            league = LeagueDAO.get_league_by_id(league_id)
        else:
            abort(400, message='Payload must contain either join_code or league_id')

        # Checking if the league exists or not
        if not league:
            abort(422, message='League does not exist. Please create one to join.')

        # Checking if user exists
        user: User = self.user_dao.get_user_by_email(email)
        if not user:
            abort(403, message=f'User with email: {email} does not exist')

        # Check if the user has already joined the league
        cnt: int = SnapshotDAO.get_count_of_user_in_snapshot(league.id, user.id)
        if cnt > 0:
            abort(403, message=f'You cannot join the same league again')

        # Check if the team trying to join exists or not, and the user is the owner or not
        team: UserTeam = self.team_dao.get_team_by_name(team_name)
        if team:
            abort(409, message=f'{team_name} already exists')

        user_team = self.team_dao.create_team(team_name, user.id)
        match_id = self.match_dao.get_current_match_id_by_status().id
        SnapshotDAO.join_league(match_id, league.id, user.id, user_team.id)
        return {
            'message': f'Successfully joined the league: {league.name} with team: {team_name}.',
            'league_id': league.id,
            'team_id': user_team.id,
            'team_name': user_team.name
        }

    def delete_league(self, league_id: int, email: str) -> dict:
        league: League = self.league_dao.get_league_by_id(league_id)

        if league:
            owner = self.user_dao.get_user_by_email(email)
            if not owner:
                abort(403, message=f'User with email: {email} does not exist')
            if league.owner == int(owner.id):
                snapshot: list[Snapshot] = self.snapshot_dao.get_league_info_by_league_id(league.id)
                self.league_dao.delete_league(snapshot, league)

                return {'message': f'{league.name} deleted successfully.'}
            abort(403, message='League can be deleted by its owner only')
        abort(403, message='The league you are trying to delete does not exist')

    def get_league_details(self, league_id: int, email: str) -> list[dict] | dict:
        user: User = self.user_dao.get_user_by_email(email)
        if not user:
            abort(403, message=f'User {email} does not exist')

        league: League = self.league_dao.get_league_by_id(league_id)

        if not league:
            abort(403, message='League does not exist')

        output = {
            'league_id': league.id,
            'league_name': league.name,
            'owner': league.owner,
            'code': league.join_code if league.join_code else ''
        }

        # match_id: int = MatchDAO.get_current_match_id_by_status().id
        # league_info: Snapshot = self.snapshot_dao.get_league_info_for_user(league.id, user.id, match_id)
        #
        league_players = []
        # if league_info or league.league_type == LeagueType.public.name:
        #
        snapshots: list[Snapshot] = self.snapshot_dao.get_league_info(league_id)
        if snapshots:
            df = pd.DataFrame([row.__dict__ for row in snapshots]).drop('_sa_instance_state', axis=1)
            df = df.loc[df.groupby(['league_id', 'team_id'])['created_at'].idxmax()]
            df['rank'] = df['cumulative_points'].rank(ascending=False).astype(int)
            result = df.sort_values('rank').to_dict('records')

            if not df.empty:
                for row in result:
                    team_id = row['team_id']
                    team: UserTeam = TeamDAO.get_team_by_id(team_id)
                    owner: User = UserDAO.get_user_by_id(team.user_id)
                    league_players.append({
                        'rank': row['rank'],
                        'team_id': team_id,
                        'team_name': team.name,
                        'team_owner': f'{owner.first_name} {owner.last_name}',
                        'remaining_subs': row['remaining_substitutes'],
                        'points': row['cumulative_points']
                    })

                output['league_players'] = league_players
                return output
        abort(403, message='Join the league to view the details.')

    def transfer_league_ownership(self, league_id: int, owner_email: str, new_owner_email: str) -> dict:
        league: League = self.league_dao.get_league_by_id(league_id)

        if league:
            owner = self.user_dao.get_user_by_email(owner_email)
            if league.owner == int(owner.id):
                new_owner = self.user_dao.get_user_by_email(new_owner_email)
                if not new_owner:
                    abort(403, message=f'User {new_owner_email} does not exist.')

                self.league_dao.transfer_league_ownership(league, new_owner.id)
                return {'message': f'New owner of {league.name} is now: {new_owner}.'}

            abort(403, message=f"League's ownership can be modified by its owner only.")
        abort(403, message=f'The league you are trying to access does not exist.')

    def get_my_leagues(self, email: str, search_obj: list[dict], page: int, size: int) -> dict:
        user: User = self.user_dao.get_user_by_email(email)
        if not user:
            abort(403, message=f'User with email: {email} does not exist')

        snapshots = SnapshotDAO.get_all_snapshots_for_user(user.id)
        df = pd.DataFrame([row.__dict__ for row in snapshots]).drop('_sa_instance_state', axis=1)
        result = df.loc[df.groupby(['league_id', 'team_id'])['created_at'].idxmax()].to_dict('records')

        # paginated_results = self.league_dao.get_paginated_my_leagues(user.id, search_obj, page, size)

        data = []

        # if len(paginated_results.items) > 0:
        #     for row in paginated_results.items:
        #         li, ul, ut, u = row
        #         data.append(
        #             {
        #                 'active': ul.is_active,
        #                 'league_id': ul.id,
        #                 'league_name': ul.name,
        #                 'type': ul.league_type.name,
        #                 'team_name': ut.name,
        #                 'team_id': ut.id,
        #                 'rank': li.rank,
        #                 'owner': ul.owner == user.id,
        #                 'remaining_subs': li.remaining_substitutes,
        #                 'points': li.cumulative_points
        #             }
        #         )
        if result:
            for row in result:
                league_id = row['league_id']
                league: League = LeagueDAO.get_league_by_id(league_id)
                team_id = row['team_id']
                team: UserTeam = TeamDAO.get_team_by_id(team_id)

                data.append(
                    {
                        'active': row['is_active'],
                        'league_id': league_id,
                        'league_name': league.name,
                        'type': league.league_type.name,
                        'team_name': team.name,
                        'team_id': team_id,
                        'rank': row['rank'],
                        'owner': league.owner == user.id,
                        'remaining_subs': row['remaining_substitutes'],
                        'points': row['cumulative_points']
                    }
                )

        # return {
        #     "data": data,
        #     "total": paginated_results.total,
        #     "total_pages": paginated_results.pages,
        #     "page": paginated_results.page,
        #     "size": paginated_results.per_page
        # }
        return {
            "data": data,
            "total": len(result),
            "total_pages": 1,
            "page": 1,
            "size": 25
        }

    def get_public_leagues(self, email: str, search_obj: list[dict], page: int, size: int) -> dict:
        user: User = self.user_dao.get_user_by_email(email)
        if not user:
            abort(403, message=f'User with email: {email} does not exist')

        paginated_results = self.league_dao.get_paginated_public_leagues(search_obj, page, size)

        data = []

        if len(paginated_results.items) > 0:
            for row in paginated_results.items:
                ul, u = row
                data.append(
                    {
                        'active': ul.is_active,
                        'league_id': ul.id,
                        'league_name': ul.name,
                        'type': ul.league_type.name,
                        'owner_id': u.id,
                        'owner_first_name': u.first_name,
                        'owner_last_name': u.last_name
                    }
                )

        return {
            "data": data,
            "total": paginated_results.total,
            "total_pages": paginated_results.pages,
            "page": paginated_results.page,
            "size": paginated_results.per_page
        }

    @staticmethod
    def calculate_fantasy_points_for_league(league_id: int, tournament_id: int = 1) -> None:
        global_rules = GlobalRulesDAO.get_all_rules()
        global_rules_map = {rule.rule: rule.id for rule in global_rules}
        league_rule_map = LeagueRulesDAO.get_league_rules_map(league_id)

        match: Match = MatchDAO.get_recent_completed_match()
        snapshots: list[Snapshot] = SnapshotDAO.get_all_rows_for_current_match_for_league(match.id, league_id)

        previous_completed_match: Match = MatchDAO.get_previous_match_of_given_match(match.id)
        previous_completed_match_points = 0

        for snapshot in snapshots:
            total_points = 0
            prediction = PredictionDAO.get_predicted_team_for_current_match(match.id,
                                                                            snapshot.user_id,
                                                                            snapshot.team_id,
                                                                            league_id)
            if prediction:
                if match.winner_team_id == prediction:
                    total_points += league_rule_map.get(global_rules_map['Correct Prediction Bonus'], 0)
                else:
                    total_points += league_rule_map.get(global_rules_map['Incorrect Prediction Bonus'], 0)

            for player in snapshot.team_snapshot:
                fantasy_points = FantasyPointsDAO.save_fantasy_points_per_player_per_league(
                    match.id, snapshot.league_id, player['id'], captain=player['captain'],
                    vice_captain=player['vice_captain']
                )
                total_points += fantasy_points

            snapshot.match_points = total_points
            if previous_completed_match:
                previous_completed_match_points = SnapshotDAO.get_row_for_team_in_league(
                    previous_completed_match.id, league_id, snapshot.team_id).cumulative_points
            snapshot.cumulative_points = snapshot.match_points + previous_completed_match_points
            snapshot.save()

        # calculating rank for each team after fantasy points update
        team_rank_map = LeagueService.calculate_rank_for_a_match(match.id, league_id)
        for snapshot in snapshots:
            snapshot.rank = team_rank_map[snapshot.team_id]
            snapshot.save()

    @staticmethod
    def calculate_rank_for_a_match(match_id: int, league_id: int) -> dict:
        snapshots: list[Snapshot] = SnapshotDAO.get_all_rows_for_current_match_for_league(match_id, league_id)
        df = pd.DataFrame([snapshot.__dict__ for snapshot in snapshots])[['team_id', 'match_points']]
        df['rank'] = df['match_points'].rank(ascending=False).astype(int)

        return df.set_index('team_id').to_dict()['rank']
