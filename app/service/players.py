from typing import Any
from flask_smorest import abort
from app.models.player import Player
from app.dao.players import PlayerDAO
from app.dao.ipl_teams import IplTeamsDAO
from app.utils.players import PlayerCategories, PlayerUtils


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
