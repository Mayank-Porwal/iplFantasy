import requests
from app.models.player import Player
from app.dao.players import PlayerDAO
from app.utils.sportsmonk import SportsMonkConstants
from app.utils.teams import get_player_object


class SportsMonkService:
    def __init__(self) -> None:
        self.player_dao = PlayerDAO

    def get_team_lineup(self, fixture_id: int, include: str = 'lineup') -> list[dict[Player]]:
        api_key = SportsMonkConstants.API_KEY
        url = f'{SportsMonkConstants.FIXTURE_URL}/{fixture_id}'  # TODO: Change this livescores url later
        params = {
            'api_token': api_key,
            'include': include
        }
        response = requests.get(url=url, params=params).json().get('data').get(include)
        output = []

        if response:
            for row in response:
                name = row['fullname']
                player = self.player_dao.get_player_by_name(name)
                if player:
                    output.append(get_player_object(player))

        return output
