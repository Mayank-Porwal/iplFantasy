from datetime import datetime
from db import db
from app.models.snapshot import Snapshot


class SnapshotDAO:
    def __init__(self):
        pass

    @staticmethod
    def get_league_info_for_user(league_id: int, user_id: int, match_id: int, active: bool = True) -> Snapshot | dict:
        info: Snapshot = Snapshot.query.filter_by(league_id=league_id, user_id=user_id, match_id=match_id,
                                                  is_active=active).first()
        return info if info else {}

    @staticmethod
    def join_league(match_id: int, league_id: int, user_id: int, team_id: int) -> None:
        join: Snapshot = Snapshot(match_id=match_id, league_id=league_id, user_id=user_id, team_id=team_id)
        join.save()

    @staticmethod
    def get_league_info_by_league_id(league_id: int, active: bool = True) -> list[Snapshot] | list:
        league_info: Snapshot = Snapshot.query.filter_by(league_id=league_id, is_active=active).all()
        return league_info if league_info else []

    @staticmethod
    def get_league_info_by_team_id(team_id: int, match_id: int, active: bool = True) -> Snapshot | dict:
        league_info: Snapshot = Snapshot.query.filter_by(match_id=match_id, team_id=team_id, is_active=active).first()
        return league_info if league_info else {}

    @staticmethod
    def get_all_league_info_by_team(team_id: int, active: bool = True) -> list[Snapshot]:
        league_info: Snapshot = Snapshot.query.filter_by(team_id=team_id, is_active=active).all()
        return league_info if league_info else []

    @staticmethod
    def set_substitutions(substitutions: int, row: Snapshot) -> None:
        row.remaining_substitutes = substitutions
        row.updated_at = datetime.utcnow()
        db.session.commit()

    @staticmethod
    def get_all_rows_for_current_match_for_league(match_id: int, league_id: int) -> list[Snapshot]:
        snapshots = Snapshot.query.filter_by(match_id=match_id, league_id=league_id).all()
        return snapshots if snapshots else []

    @staticmethod
    def get_count_of_user_in_snapshot(league_id: int, user_id: int, active: bool = True) -> int:
        cnt: int = Snapshot.query.filter_by(league_id=league_id, user_id=user_id, is_active=active).count()
        return cnt

    @staticmethod
    def get_row_for_team_in_league(match_id: int, league_id: int, team_id: int, active: bool = True):
        row: Snapshot = Snapshot.query.filter_by(match_id=match_id, league_id=league_id, team_id=team_id,
                                                 is_active=active).first()
        return row if row else {}

    @staticmethod
    def submit_team(snapshot: Snapshot, draft_team: dict) -> None:
        snapshot.team_snapshot = draft_team
        snapshot.save()
