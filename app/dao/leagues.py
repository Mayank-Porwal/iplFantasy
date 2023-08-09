from db import db, conn
from app.models.leagues import UserLeague, LeagueInfo
from app.dao.users import UserDAO
from app.utils.common_utils import generate_uuid


class LeagueDAO:
    def __init__(self):
        self.user_dao = UserDAO

    @staticmethod
    def get_league_by_name(league_name: str, active: bool = True) -> UserLeague:
        league: UserLeague = UserLeague.query.filter_by(name=league_name, is_active=active).first()
        return league if league else {}

    @staticmethod
    def get_league_by_code(code: str, active: bool = True) -> UserLeague:
        league: UserLeague = UserLeague.query.filter_by(join_code=code, is_active=active).first()
        return league if league else {}

    @staticmethod
    def get_league_info_by_user(league_id: int, user_id: int, active: bool = True) -> LeagueInfo:
        league_info: LeagueInfo = LeagueInfo.query.filter_by(league_id=league_id, user_id=user_id, is_active=active).\
            first()
        return league_info if league_info else {}

    @staticmethod
    def get_all_league_info_by_team(team_id: int, active: bool = True) -> list[LeagueInfo]:
        league_info: LeagueInfo = LeagueInfo.query.filter_by(team_id=team_id, is_active=True).all()
        return league_info if league_info else []

    @staticmethod
    def get_all_league_info_by_league(league_id: int, active: bool = True) -> list[LeagueInfo]:
        league_info: LeagueInfo = LeagueInfo.query.filter_by(league_id=league_id, is_active=active).all()
        return league_info if league_info else []

    @staticmethod
    def join_league(league_id: int, user_id: int, team_id: int) -> None:
        join: LeagueInfo = LeagueInfo(league_id=league_id, user_id=user_id, team_id=team_id)
        join.save()

    @staticmethod
    def create_league(league_name: str, league_type: str, user_id: int, join_code_flag: bool) -> None:
        if not join_code_flag:
            league: UserLeague = UserLeague(name=league_name, owner=int(user_id), league_type=league_type)
        else:
            league: UserLeague = UserLeague(name=league_name, owner=int(user_id), league_type=league_type,
                                            join_code=generate_uuid())

        league.save()

    @staticmethod
    def delete_league(league_info_list: list[LeagueInfo], league: UserLeague) -> None:
        if league_info_list:
            for row in league_info_list:
                row.is_active = False

        league.is_active = False
        db.session.commit()

    @staticmethod
    def get_league_details(league_name: str) -> list[tuple]:
        query = f"""
        select team_rank, ut.name as team_name, u.first_name || ' ' || u.last_name as owner, substitutes, team_points
        from league_info li
        join user_league ul 
        on li.league_id = ul.id 
        join user_team ut 
        on ut.id = li.team_id
        join public."user" u 
        on u.id = ut.user_id 
        where ul."name" = '{league_name}'
        ;
    """
        result = conn().execute(query).fetchall()
        return result

    @staticmethod
    def transfer_league_ownership(league: UserLeague, new_owner_id: int) -> None:
        league.owner = int(new_owner_id)
        db.session.commit()

    @staticmethod
    def rollback_league(league: UserLeague) -> None:
        UserLeague.query.filter_by(id=league.id).delete()
        db.session.commit()
