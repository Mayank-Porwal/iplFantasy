from app.models.player import Player


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
    def get_players_by_category(category: str) -> list[Player]:
        players: list = Player.query.filter_by(category=category.lower()).all()
        return players if players else []

    @staticmethod
    def get_players_by_team(team: str) -> list[Player]:
        players: list = Player.query.filter_by(ipl_team=team.upper()).all()
        return players if players else []
