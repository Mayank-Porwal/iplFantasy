import requests

from typing import Any
from flask_smorest import abort
from app.models.player import Player
from app.dao.players import PlayerDAO
from app.dao.ipl_teams import IplTeamsDAO
from app.utils.players import PlayerCategories, PlayerUtils
from app.utils.sportsmonk import SportsMonkConstants


class PlayerService:
    def __init__(self) -> None:
        self.dao = PlayerDAO

    def get_all_players(self) -> list[dict[str, Any]] | dict:
        players: list[Player] = self.dao.get_all_players()
        if not players:
            abort(500, message='Something went wrong.')

        output = []
        for player in players:
            row = PlayerUtils.convert_object_to_dict(player)
            output.append(row)

        return output

    def get_player_by_id(self, player_id: int) -> dict[str, Any]:
        player = self.dao.get_player_by_id(player_id)
        if not player:
            abort(404, message='Player not found.')

        return PlayerUtils.convert_object_to_dict(player)

    def get_all_players_by_category(self, category: str) -> list[dict[str, Any]] | dict:
        if category.lower() not in PlayerCategories.get_all_categories():
            abort(422, message='Invalid Category.')

        category_id: list[int] = PlayerCategories.get_category_id_by_name_map()[category]
        players = self.dao.get_players_by_category(category_id)
        if not players:
            abort(500, message='Something went wrong.')

        output = []
        for player in players:
            row = PlayerUtils.convert_object_to_dict(player)
            output.append(row)

        return output

    def get_all_players_by_team(self, team: str) -> list[dict[str, Any]] | dict:
        team_id = IplTeamsDAO.get_id_from_team_name(team)
        players = self.dao.get_players_by_team(team_id)
        if not players:
            abort(404, message='Invalid team.')

        output = []
        for player in players:
            row = PlayerUtils.convert_object_to_dict(player)
            output.append(row)

        return output

    def save_all_players(self) -> dict:
        ipl_teams_ids = IplTeamsDAO.get_active_ipl_team_ids()
        players_data = []

        if not ipl_teams_ids:
            abort(404, message='IPL team ids not found in DB')

        for ipl_team_id in ipl_teams_ids:
            params = {'api_token': SportsMonkConstants.API_KEY}
            url = f'{SportsMonkConstants.BASE_URL}/teams/{ipl_team_id}/squad/1484'
            data = requests.get(url=url, params=params).json().get('data')

            if not data:
                abort(404, message='Could not fetch data from 3rd party teams endpoint')

            squad_data = data['squad']

            for player in squad_data:
                player_data = {
                    'id': player['id'],
                    'name': player['fullname'],
                    'category': player['position']['id'],
                    'ipl_team': ipl_team_id,
                    'cap': 6,
                    'image_file': player['image_path']
                }
                players_data.append(player_data)

        if not players_data:
            abort(404, message='Could not fetch data from 3rd party teams endpoint')

        self.dao.create_all_players(players_data)
        return {'message': 'Successfully inserted all player data'}
