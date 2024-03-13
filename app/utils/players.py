from typing import Any
from app.models.player import Player
from app.dao.ipl_teams import IplTeamsDAO


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
            11: PlayerCategories.AR,
            8: PlayerCategories.BAT
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
    def convert_object_to_dict(player: Player) -> dict[str, Any]:
        categories = PlayerCategories.get_sportsmonk_categories_map()
        ipl_teams_name_map = IplTeamsDAO.get_id_to_team_name_map()
        ipl_teams_img_map = IplTeamsDAO.get_team_logo_to_team_id_map()

        return {
            'cap': player.cap,
            'category': categories[player.category] if categories else player.category,
            'id': player.id,
            'image_file': player.image_file,
            'name': player.name,
            'ipl_team': ipl_teams_name_map[player.ipl_team] if ipl_teams_name_map else player.ipl_team,
            'ipl_team_img': ipl_teams_img_map[player.ipl_team] if ipl_teams_img_map else ''
        }
