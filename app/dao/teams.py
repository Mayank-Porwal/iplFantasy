from db import db
from app.models.teams import UserTeam
from app.models.leagues import LeagueInfo


class TeamDAO:
    @staticmethod
    def get_team_by_name(name: str, active: bool = True) -> UserTeam:
        team: UserTeam = UserTeam.query.filter_by(name=name, is_active=active).first()
        return team if team else {}

    @staticmethod
    def create_team(team_name: str, players: dict, user_id: int) -> None:
        team: UserTeam = UserTeam(name=team_name, players=players, user_id=user_id)
        team.save()

    @staticmethod
    def delete_team(league_info: list[LeagueInfo], team: UserTeam) -> None:
        if league_info:
            for row in league_info:
                row.is_active = False

        team.is_active = False
        db.session.commit()

    @staticmethod
    def get_all_user_teams(user_id: int) -> list[UserTeam]:
        teams = UserTeam.query.filter_by(user_id=user_id, is_active=True).all()
        return teams if teams else []
