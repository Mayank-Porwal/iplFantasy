from flask_smorest import abort
from app.models.snapshot import Snapshot
from app.models.match import Match
from app.models.leagues import League
from app.dao.leagues import LeagueDAO
from app.dao.teams import TeamDAO
from app.dao.snapshot import SnapshotDAO
from app.dao.match import MatchDAO


class SnapshotService:
    def __init__(self) -> None:
        self.dao = SnapshotDAO

    def submit_all_teams_for_league(self, match_id: int, league_id: int) -> dict:
        match: Match = MatchDAO.get_match_by_id(match_id)
        if not match:
            abort(403, message=f'Match does not exist')

        league: League = LeagueDAO.get_league_by_id(league_id)
        if not league:
            abort(403, message=f'League does not exist')

        snapshots: list[Snapshot] = self.dao.get_all_rows_for_current_match_for_league(match_id, league_id)
        if not snapshots:
            abort(403, message=f'No teams have joined this league for this match')

        try:
            for snapshot in snapshots:
                team = TeamDAO.get_team_by_id(snapshot.team_id)
                if not team:
                    abort(403, message=f'Team does not exist')

                self.dao.submit_team(snapshot, team.draft_players)
            return {'message': 'Successfully submitted all teams for league.'}
        except Exception as e:
            abort(403, message=f'Failed with error: {e}')
