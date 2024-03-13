from app.models.player import Player
from db import db


class PlayerDAO:
    @staticmethod
    def get_list_of_players(player_ids: list[int]) -> list[Player]:
        players: list = Player.query.filter(Player.id.in_(player_ids)).all()
        return players if players else []

    @staticmethod
    def get_all_players() -> list[Player]:
        players: list = Player.query.all()
        return players if players else []

    @staticmethod
    def get_player_by_id(player_id: int) -> Player:
        return Player.query.get(player_id)

    @staticmethod
    def get_players_by_category(category_id: list[int]) -> list[Player]:
        players: list = Player.query.filter(Player.category.in_(category_id)).all()
        return players if players else []

    @staticmethod
    def get_players_by_team(team_id: int | list) -> list[Player]:
        players = None
        if isinstance(team_id, list):
            players = Player.query.filter(Player.ipl_team.in_(team_id)).all()
        elif isinstance(team_id, int):
            players = Player.query.filter_by(ipl_team=team_id).all()

        return players if players else []

    @staticmethod
    def get_player_by_name(name: str) -> Player:
        player: Player = Player.query.filter(Player.name.ilike(f'%{name}%')).first()
        return player if player else {}

    @staticmethod
    def create_player(player_data: dict) -> None:
        player: Player = Player(**player_data)
        player.save()

    @staticmethod
    def create_all_players(player_data: list[dict]) -> None:
        if player_data:
            for row in player_data:
                player: Player = Player(**row)
                db.session.add(player)

            db.session.commit()
