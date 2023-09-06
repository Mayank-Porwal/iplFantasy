import pandas as pd
from flask_smorest import abort
from app.dao.players import PlayerDAO
from app.dao.ipl_teams import IplTeamsDAO
from app.utils.players import PlayerUtils, PlayerCategories


def get_player_object(player) -> dict:
    return {
        'id': player.id,
        'name': player.name,
        'cap': player.cap,
        'category': player.category,
        'img': player.image_file,
        'team': player.ipl_team
    }


class TeamUtils:
    def __init__(self):
        pass

    @staticmethod
    def create_team_players_dict(players):
        player_ids = [player['id'] for player in players]
        players_list = PlayerDAO.get_list_of_players(player_ids)
        if not players_list:
            abort(422, message='Invalid data from 3rd party APIs')

        output = []
        for player in players_list:
            row = PlayerUtils.convert_object_to_dict(player)
            output.append(row)

        players_df = pd.DataFrame(output)
        team_df = pd.DataFrame(players)
        final_df = players_df.merge(team_df, on='id')

        return final_df.to_dict('records')
