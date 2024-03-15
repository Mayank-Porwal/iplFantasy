import requests
from flask_smorest import abort
from app.dao.match import MatchDAO
from app.dao.ipl_teams import IplTeamsDAO
from app.utils.sportsmonk import SportsMonkConstants
from app.utils.match import MatchStatus


class MatchService:
    def __init__(self) -> None:
        self.dao = MatchDAO

    def create_all_fixtures(self, tournament_id: int, tournament_type: str = 'T20')\
            -> dict:
        params = {
            'api_token': SportsMonkConstants.API_KEY,
            'page': 15,
            'filter[type]': tournament_type
        }
        data = requests.get(url=SportsMonkConstants.FIXTURE_URL, params=params).json().get('data')

        if not data:
            abort(404, message='Could not fetch data from Sportsmonk fixtures endpoint.')

        match_statuses: list = MatchStatus.all_statuses()

        for row in data:
            if row['league_id'] == 1:
                if row['status'] == 'Aban.':
                    status = 4
                elif not row['status'].upper() in match_statuses:
                    status = -1
                else:
                    status = MatchStatus[row['status'].upper()].value

                fixture_data = {
                    'id': row['id'],
                    'tournament_id': tournament_id,
                    'home_team_id': row['localteam_id'],
                    'away_team_id': row['visitorteam_id'],
                    'venue_id': row['venue_id'],
                    'schedule': row['starting_at'],
                    'status': status,
                    'season_id': row['season_id']
                }

                fixture = self.dao.get_match_by_id(row['id'])
                if not fixture:
                    self.dao.create_fixture(fixture_data)

        return {'message': 'Created all fixtures successfully'}

    def get_lineup_for_a_match(self) -> list[dict] | dict:
        matches: list = self.dao.get_upcoming_matches_by_status()

        params = {
            'api_token': SportsMonkConstants.API_KEY,
            'include': 'lineup'
        }

        output = []
        for c, match in enumerate(matches):
            data = {}
            if c == 0:
                url: str = f'{SportsMonkConstants.FIXTURE_URL}/{match.id}'  # TODO: Change to livescores api
                data: dict = requests.get(url=url, params=params).json().get('data')

            home_team = IplTeamsDAO.get_ipl_team_by_id(match.home_team_id)
            away_team = IplTeamsDAO.get_ipl_team_by_id(match.away_team_id)

            result = {
                    'teamA': {
                        'name': home_team.code,
                        'image': home_team.image,
                        'players': []
                    },
                    'teamB': {
                        'name': away_team.code,
                        'image': away_team.image,
                        'players': []
                    },
                    'match_time': match.schedule
                }

            # if not data or not data['lineup']:
            #     return output
            if data.get('lineup'):
                home_team_players, away_team_players = [], []
                for player in data['lineup']:
                    if player['lineup']['team_id'] == match.home_team_id:
                        home_team_players.append(player.id)
                    elif player['lineup']['team_id'] == match.away_team_id:
                        away_team_players.append(player.id)

                result['teamA']['players'] = home_team_players
                result['teamB']['players'] = away_team_players

            output.append(result)

        return output
