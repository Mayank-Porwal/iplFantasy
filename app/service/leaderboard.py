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


class LeaderBoardService:
    @staticmethod
    def get_match_leader_board(league_id: int, email: str, tournament_id: int = 1):
        match: Match = MatchDAO.get_current_match_id_by_status(status='FINISHED')
        if not match:
            abort(403, message=f'Match is in-progress. Please visit this page post completion.')

        user: User = UserDAO.get_user_by_email(email)
        if not user:
            abort(403, message=f'User {email} does not exist')

        league: League = LeagueDAO.get_league_by_id(league_id)

        if not league:
            abort(403, message='League does not exist')

        snapshots: list[Snapshot] = SnapshotDAO.get_all_rows_for_current_match(match.id)
        if not snapshots:
            abort(403, message='No teams are part of this league')

        output = []
        for snapshot in snapshots:
            team_snapshot = snapshot.team_snapshot
            if not team_snapshot:
                abort(403, message=f'No players found in team: {snapshot.team_id} for this match')

            team_output = []
            for player in team_snapshot:
                player_id = player.get('id')
                score: Scores = ScoresDAO.get_scores_for_a_player(tournament_id, match.id, player_id)
                points = score.fantasy_points if score else '-'
                team_output.append({
                    'id': player_id,
                    'name': PlayerDAO.get_player_by_id(player_id).name,
                    'points': points
                })

            output.append(
                {
                    'team_id': snapshot.team_id,
                    'team_name': '',
                    'owner': '',
                    'data': team_output
                }
            )

        return output
