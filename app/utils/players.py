from typing import Any
from app.models.player import Player


class PlayerCategories:
    WK: str = 'wk'
    BWL: str = 'bowler'
    AR: str = 'ar'
    BAT: str = 'batsman'

    @classmethod
    def get_all_categories(cls) -> list[str]:
        return [value for name, value in vars(cls).items() if name.isupper()]

    @classmethod
    def get_sportsmonk_categories_map(cls) -> dict[int, str]:
        return {
            1: PlayerCategories.BAT,
            14: PlayerCategories.AR,
            3: PlayerCategories.WK,
            2: PlayerCategories.BWL,
            4: PlayerCategories.AR,
            11: PlayerCategories.AR
        }

    @classmethod
    def get_category_id_by_name_map(cls) -> dict[str, list[int]]:
        return {
            PlayerCategories.BAT: [1],
            PlayerCategories.BWL: [2],
            PlayerCategories.WK: [3],
            PlayerCategories.AR: [4, 11, 14]
        }


class PlayerUtils:
    @staticmethod
    def convert_object_to_dict(player: Player, **kwargs) -> dict[str, Any]:
        categories = kwargs.get('categories')
        ipl_teams_map = kwargs.get('ipl_teams_map')

        return {
            'cap': player.cap,
            'category': categories[player.category] if categories else player.category,
            'id': player.id,
            'image_file': player.image_file,
            'name': player.name,
            'ipl_team': ipl_teams_map[player.ipl_team] if ipl_teams_map else player.ipl_team
        }
