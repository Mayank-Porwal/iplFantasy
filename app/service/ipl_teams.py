import requests
from flask_smorest import abort
from app.dao.ipl_teams import IplTeamsDAO
from app.dao.players import PlayerDAO
from app.utils.sportsmonk import SportsMonkConstants


class IplTeamsService:
    def __init__(self) -> None:
        self.dao = IplTeamsDAO
        self.player_dao = PlayerDAO

    def create_all_teams(self, season_id: int = 1223) -> dict:
        params = {
            'api_token': SportsMonkConstants.API_KEY,
            'filter[country_id]': 153732,
            'include': 'squad'
        }
        data = requests.get(url=SportsMonkConstants.TEAMS_URL, params=params).json().get('data')

        if not data:
            abort(404, message='Could not fetch data from Sportsmonk teams endpoint.')

        for row in data:
            fixture_data = {
                'id': row['id'],
                'name': row['name'],
                'code': row['code'],
                'image': row['image_path']
            }

            ipl_team = self.dao.get_ipl_team_by_id(row['id'])
            if not ipl_team:
                self.dao.create_ipl_team(fixture_data)

            for player in row['squad']:
                if player['squad']['season_id'] == season_id:
                    player_data = {
                        'id': player['id'],
                        'name': player['fullname'],
                        'category': player['position']['id'],
                        'ipl_team': row['id'],
                        'cap': 6,
                        'image_file': player['image_path']
                    }

                    current_player = self.player_dao.get_player_by_id(player['id'])
                    if not current_player:
                        self.player_dao.create_player(player_data)

        return {'message': 'Successfully inserted all ipl teams'}
