from flask_smorest import abort
from app.models.leagues import League
from app.models.users import User
from app.models.snapshot import Snapshot
from app.models.match import Match
from app.models.scores import Scores
from app.dao.leagues import LeagueDAO
from app.dao.users import UserDAO
from app.dao.snapshot import SnapshotDAO
from app.dao.match import MatchDAO
from app.dao.scores import ScoresDAO
from app.dao.players import PlayerDAO
from app.dao.teams import TeamDAO
from app.dao.fantasy_points import FantasyPointsDAO, FantasyPoints


class LeaderBoardService:
    @staticmethod
    def get_match_leader_board(match_id: int, league_id: int, email: str, tournament_id: int = 1):
        match: Match = MatchDAO.get_match_by_id(match_id)
        if not match:
            abort(403, message=f'Match does not exist')

        user: User = UserDAO.get_user_by_email(email)
        if not user:
            abort(403, message=f'User {email} does not exist')

        league: League = LeagueDAO.get_league_by_id(league_id)

        if not league:
            abort(403, message='League does not exist')

        snapshots: list[Snapshot] = SnapshotDAO.get_all_rows_for_current_match_for_league(match_id, league_id)
        if not snapshots:
            abort(403, message='No teams are part of this league')

        previous_match: Match = MatchDAO.get_previous_match_of_given_match(match_id)
        trades = 0

        output = []
        for snapshot in snapshots:
            team_snapshot = snapshot.team_snapshot
            if not team_snapshot:
                abort(403, message=f'No players found in team: {snapshot.team_id} for this match')

            team_output = []
            for player in team_snapshot:
                player_id = player.get('id')
                score: FantasyPoints = FantasyPointsDAO.get_fantasy_points_of_player_in_league(match.id, league_id,
                                                                                               player_id)
                points = score.points if score else 0.0
                if player.get('captain'):
                    points *= 2
                elif player.get('vice_captain'):
                    points *= 1.5

                team_output.append({
                    'id': player_id,
                    'name': PlayerDAO.get_player_by_id(player_id).name,
                    'points': points
                })

            user: User = UserDAO.get_user_by_id(snapshot.user_id)
            user_name: str = f'{user.first_name} {user.last_name}'

            if previous_match:
                previous_snapshot: Snapshot = SnapshotDAO.get_row_for_team_in_league(previous_match.id, league_id,
                                                                                     snapshot.team_id)
                trades = snapshot.remaining_substitutes - previous_snapshot.remaining_substitutes

            output.append(
                {
                    'team_id': snapshot.team_id,
                    'team_name': TeamDAO.get_team_by_id(snapshot.team_id).name,
                    'owner': user_name,
                    'owner_id': user.id,
                    'trades': trades,
                    'total_points': snapshot.match_points,
                    'rank': snapshot.rank,
                    'data': team_output
                }
            )

        return output
