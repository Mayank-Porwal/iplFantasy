from enum import Enum
from flask_smorest import abort


class LeagueType(Enum):
    private: int = 0
    public: int = 1


class MyLeaguesAllowedFilterFields:
    OWNER = 'owner'
    LEAGUE_NAME = 'league_name'
    LEAGUE_TYPE = 'league_type'
    IS_LEAGUE_ACTIVE = 'active'
    FIRST_NAME = 'owner_first_name'
    LAST_NAME = 'owner_last_name'

    @classmethod
    def get_allowed_filter_fields(cls) -> list:
        return [value for name, value in vars(cls).items() if name.isupper()]


class LeagueUtils:
    @staticmethod
    def create_search_filters(search_obj: list[dict], user_id: int = None) -> list | dict:
        from app.models.leagues import League
        from app.models.users import User

        filters: list = []

        for obj in search_obj:
            field: str = obj.get('field')
            if field not in MyLeaguesAllowedFilterFields.get_allowed_filter_fields():
                abort(422, message='Invalid field in search_obj payload.')

            if field == MyLeaguesAllowedFilterFields.OWNER:
                filter_operator: str = obj.get('operator')
                if filter_operator != 'equals':
                    abort(422, message='Invalid operator for field="owner" in payload. Expected is "equals".')

                value: bool = obj.get('value')
                if not isinstance(value, bool):
                    abort(422, message='Invalid type of value for field="owner". Expected is a boolean.')

                if value:
                    filters.append(f' and {League.__tablename__}.owner = {user_id}')

            if field == MyLeaguesAllowedFilterFields.LEAGUE_NAME:
                sql_operator = '='
                filter_operator: str = obj.get('operator')

                value: str = obj.get('value')
                if not isinstance(value, str):
                    abort(422, message='Invalid type of value for field="league_name". Expected is a string.')

                if filter_operator == 'contains':
                    sql_operator = 'ilike'
                    filters.append(f" and {League.__tablename__}.name {sql_operator} '%{value}%'")
                else:
                    filters.append(f" and {League.__tablename__}.name {sql_operator} '{value}'")

            if field == MyLeaguesAllowedFilterFields.LEAGUE_TYPE:
                filter_operator: str = obj.get('operator')
                if filter_operator != 'equals':
                    abort(422, message='Invalid operator for field="league_name" in payload. Expected is "equals".')

                value: bool = obj.get('value')
                if not isinstance(value, bool):
                    abort(422, message='Invalid type of value for field="league_name". Expected is a boolean.')

                if value:
                    filters.append(f" and {League.__tablename__}.league_type = '{LeagueType.private.name}'")
                else:
                    filters.append(f" and {League.__tablename__}.league_type = '{LeagueType.public.name}'")

            if field == MyLeaguesAllowedFilterFields.IS_LEAGUE_ACTIVE:
                filter_operator: str = obj.get('operator')
                if filter_operator != 'equals':
                    abort(422, message='Invalid operator for field="active" in payload. Expected is "equals".')

                value: bool = obj.get('value')
                if not isinstance(value, bool):
                    abort(422, message='Invalid type of value for field="active". Expected is a boolean.')

                filters.append(f' and {League.__tablename__}.is_active = {value}')

            if field == MyLeaguesAllowedFilterFields.FIRST_NAME:
                filter_operator: str = obj.get('operator')
                if filter_operator != 'contains':
                    abort(422, message='Invalid operator for field="first_name" in payload. '
                                       'Expected is "contains".')

                value: str = obj.get('value')
                if not isinstance(value, str):
                    abort(422, message='Invalid type of value for field="owner". Expected is a string.')

                if value:
                    filters.append(f" and \"{User.__tablename__}\".first_name ilike '%{value}%'")

            if field == MyLeaguesAllowedFilterFields.LAST_NAME:
                filter_operator: str = obj.get('operator')
                if filter_operator != 'contains':
                    abort(422, message='Invalid operator for field="last_name" in payload. '
                                       'Expected is "contains".')

                value: str = obj.get('value')
                if not isinstance(value, str):
                    abort(422, message='Invalid type of value for field="owner". Expected is a string.')

                if value:
                    filters.append(f" and \"{User.__tablename__}\".last_name ilike '%{value}%'")

        return filters
