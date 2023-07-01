import uuid
from enum import Enum


class LeagueType(Enum):
    private = 0
    public = 1


def get_league_object(league):
    return {'id': league.id, 'name': league.name, 'owner': league.owner}


def generate_uuid():
    return uuid.uuid4().hex[:5].upper()

