from datetime import datetime
from db import db
from app.models.teams import UserTeam
from app.models.snapshot import Snapshot


class TeamDAO:
    @staticmethod
    def get_team_by_name(name: str, active: bool = True) -> UserTeam:
        team: UserTeam = UserTeam.query.filter_by(name=name, is_active=active).first()
        return team if team else {}

    @staticmethod
    def get_team_by_id(team_id: int, active: bool = True) -> UserTeam:
        team: UserTeam = UserTeam.query.filter_by(id=team_id, is_active=active).first()
        return team if team else {}

    @staticmethod
    def create_team(team_name: str, user_id: int) -> UserTeam:
        team: UserTeam = UserTeam(name=team_name, user_id=user_id)
        team.save()

        return team

    @staticmethod
    def delete_team(league_info: list[Snapshot], team: UserTeam) -> None:
        if league_info:
            for row in league_info:
                row.is_active = False

        team.is_active = False
        db.session.commit()

    @staticmethod
    def edit_team(team: UserTeam, players: dict) -> None:
        team.draft_players = players
        team.updated_at = datetime.utcnow()
        db.session.commit()

    @staticmethod
    def get_all_user_teams(user_id: int) -> list[UserTeam]:
        teams = UserTeam.query.filter_by(user_id=user_id, is_active=True).all()
        return teams if teams else []
