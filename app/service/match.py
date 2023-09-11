import requests
from flask_smorest import abort
from app.dao.match import MatchDAO
from app.dao.players import PlayerDAO
from app.utils.sportsmonk import SportsMonkConstants
from app.utils.match import MatchStatus
from app.utils.players import PlayerUtils


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

    def get_lineup_for_a_match(self) -> list[dict] | dict:
        match_id = self.dao.get_current_match_id_by_status().id
        params = {
            'api_token': SportsMonkConstants.API_KEY,
            'include': 'lineup'
        }

        url: str = f'{SportsMonkConstants.FIXTURE_URL}/{match_id}'  # TODO: Change to livescores api
        data: dict = requests.get(url=url, params=params).json().get('data')

        if not data:
            abort(404, message='Data not found')

        playing_team_ids = [data['localteam_id'], data['visitorteam_id']]
        squad = PlayerDAO.get_players_by_team(playing_team_ids)

        lineup: list[dict] = data.get('lineup')
        if not lineup:
            abort(404, message='Lineup not available yet. Please try later.')

        player_ids: list[int] = [row['id'] for row in lineup]

        output = []
        for player in squad:
            row = PlayerUtils.convert_object_to_dict(player)
            if row['id'] in player_ids:
                row['playing'] = True
            else:
                row['playing'] = False
            output.append(row)

        return output
