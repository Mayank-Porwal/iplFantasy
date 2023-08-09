from flask_smorest import abort
from app.models.player import Player
from app.dao.players import PlayerDAO
from app.utils.players import PlayerCategories


class PlayerService:
    def __init__(self) -> None:
        self.dao = PlayerDAO

    def get_all_players(self) -> list[Player] | dict:
        players = self.dao.get_all_players()
        if not players:
            abort(500, message='Something went wrong.')
        return players

    def get_player_by_id(self, player_id: int) -> Player | dict:
        player = self.dao.get_player_by_id(player_id)
        if not player:
            abort(404, message='Player not found.')
        return player

    def get_all_players_by_category(self, category: str) -> list[Player] | dict:
        if category.lower() not in PlayerCategories.get_all_categories():
            abort(422, message='Invalid Category.')

        players = self.dao.get_players_by_category(category)
        if not players:
            abort(500, message='Something went wrong.')
        return players

    def get_all_players_by_team(self, team: str) -> list[Player] | dict:
        players = self.dao.get_players_by_team(team)
        if not players:
            abort(404, message='Invalid team.')
        return players
