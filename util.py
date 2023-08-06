import uuid
from enum import Enum
from flask_smorest import abort
from flask_jwt_extended import get_jwt_identity


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


def fetch_user_from_jwt():
    email = get_jwt_identity().get('email')
    if not email:
        abort(498, message='invalid token')
    return email
