import sqlalchemy.orm

from db import db
from app.models.leagues import League
from app.models.teams import UserTeam
from app.models.users import User
from app.models.snapshot import Snapshot
from app.dao.users import UserDAO
from app.utils.common_utils import generate_uuid
from app.utils.leagues import LeagueUtils
from sqlalchemy import text


class LeagueDAO:
    def __init__(self):
        self.user_dao = UserDAO

    @staticmethod
    def get_league_by_name(league_name: str, active: bool = True) -> League:
        league: League = League.query.filter_by(name=league_name, is_active=active).first()
        return league if league else {}

    @staticmethod
    def get_league_by_id(league_id: int, active: bool = True) -> League:
        league: League = League.query.filter_by(id=league_id, is_active=active).first()
        return league if league else {}

    @staticmethod
    def get_league_by_code(code: str, active: bool = True) -> League:
        league: League = League.query.filter_by(join_code=code, is_active=active).first()
        return league if league else {}

    @staticmethod
    def create_league(tournament_id: int, league_name: str, league_type: str, user_id: int, join_code_flag: bool) \
            -> League:
        if not join_code_flag:
            league: League = League(tournament_id=tournament_id, name=league_name, owner=int(user_id),
                                    league_type=league_type)
        else:
            league: League = League(tournament_id=tournament_id, name=league_name, owner=int(user_id),
                                    league_type=league_type, join_code=generate_uuid())

        league.save()
        return league

    @staticmethod
    def delete_league(league_info_list: list[Snapshot], league: League) -> None:
        if league_info_list:
            for row in league_info_list:
                row.is_active = False

        league.is_active = False
        db.session.commit()

    @staticmethod
    def get_league_details(league_id: int, match_id: int) -> list[tuple]:
        result: list = (db.session.query(Snapshot, League, UserTeam, User)
                        .join(League, League.id == Snapshot.league_id)
                        .join(UserTeam, UserTeam.id == Snapshot.team_id)
                        .join(User, User.id == Snapshot.user_id)
                        .filter(League.id == league_id, Snapshot.match_id == match_id))

        return result

    @staticmethod
    def transfer_league_ownership(league: League, new_owner_id: int) -> None:
        league.owner = int(new_owner_id)
        db.session.commit()

    @staticmethod
    def rollback_league(league: League) -> None:
        League.query.filter_by(id=league.id).delete()
        db.session.commit()

    @staticmethod
    def get_paginated_my_leagues(user_id: int, search_obj: list[dict], page: int = 1, size: int = 2) -> \
            sqlalchemy.orm.Query:
        filters: list = [f'"{User.__tablename__}".id = {user_id}']

        if search_obj:
            search_filters: list = LeagueUtils.create_search_filters(search_obj, user_id=user_id)
            filters.extend(search_filters)

        query: sqlalchemy.orm.Query = db.session.query(Snapshot, League, UserTeam, User)\
            .join(League, League.id == Snapshot.league_id)\
            .join(UserTeam, UserTeam.id == Snapshot.team_id)\
            .join(User, User.id == Snapshot.user_id)\
            .filter(text(''.join(filters)))

        print(str(query))

        return query.paginate(page=page, per_page=size)
