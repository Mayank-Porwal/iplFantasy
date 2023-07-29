import uuid
from enum import Enum


class LeagueType(Enum):
    private = 0
    public = 1


def get_league_object(league):
    return {'id': league.id, 'name': league.name, 'owner': league.owner}


def generate_uuid():
    return uuid.uuid4().hex[:5].upper()


def get_player_object(player):
    return {'id': player.id, 'name': player.name, 'cap': player.cap, 'category': player.category,
            'img': player.image_file, 'team': player.ipl_team}
