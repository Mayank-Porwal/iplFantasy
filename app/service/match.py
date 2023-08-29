import requests
from flask_smorest import abort
from app.dao.match import MatchDAO
from app.utils.sportsmonk import SportsMonkConstants
from app.utils.match import MatchStatus


class MatchService:
    def __init__(self) -> None:
        self.dao = MatchDAO

    def create_all_fixtures(self, tournament_id: int, start_date: str, end_date: str, tournament_type: str = 'T20')\
            -> dict:
        params = {
            'api_token': SportsMonkConstants.API_KEY,
            'filter[starts_between]': f'{start_date},{end_date}',
            'filter[type]': tournament_type
        }
        data = requests.get(url=SportsMonkConstants.FIXTURE_URL, params=params).json().get('data')

        if not data:
            abort(404, message='Could not fetch data from Sportsmonk fixtures endpoint.')

        match_statuses: list = MatchStatus.all_statuses()

        for row in data:
            if row['status'] == 'Aban.':
                status = 4
            elif not row['status'].upper() in match_statuses:
                status = -1
            else:
                status = MatchStatus[row['status'].upper()].value

            fixture_data = {
                'id': row['id'],
                'tournament_id': tournament_id,
                'home_team_id': row['localteam_id'],
                'away_team_id': row['visitorteam_id'],
                'venue_id': row['venue_id'],
                'schedule': row['starting_at'],
                'status': status,
                'season_id': row['season_id']
            }

            fixture = self.dao.get_match_by_id(row['id'])
            if not fixture:
                self.dao.create_fixture(fixture_data)

        return {'message': 'Created all fixtures successfully'}
