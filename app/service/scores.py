import requests
from flask_smorest import abort

from app.dao.leagues import LeagueDAO
from app.dao.scores import ScoresDAO
from app.dao.match import MatchDAO
from app.dao.snapshot import SnapshotDAO
from app.dao.rules import LeagueRulesDAO
from app.models.match import Match
from app.models.snapshot import Snapshot
from app.models.scores import Scores
from app.dao.users import UserDAO
from app.dao.prediction import PredictionDAO
from app.utils.sportsmonk import SportsMonkConstants


class ScoreService:
    def __init__(self) -> None:
        self.dao = ScoresDAO

    def upsert_scores_of_players(self, tournament_id: int = 1) -> None:
        match_id: int = MatchDAO.get_current_match_id_by_status().id

        url = f'{SportsMonkConstants.FIXTURE_URL}/{match_id}'
        params = {
            'api_token': SportsMonkConstants.API_KEY,
            'include': 'batting, bowling, manofmatch, manofseries'
        }

        data = requests.get(url=url, params=params).json().get('data')
        if not data:
            abort(404, message='Could not fetch data from 3rd party fixtures endpoint')

        batting_data = data.get('batting')
        bowling_data = data.get('bowling')
        man_of_match_player_id = data.get('man_of_match_id')

        if man_of_match_player_id:
            self.dao.upsert_man_of_the_match_score(tournament_id, match_id, man_of_match_player_id)

        if batting_data:
            for batsman in batting_data:
                batsman_id = batsman.get('player_id')
                data = {
                    'runs_scored': batsman.get('score'),
                    'balls_faced': batsman.get('ball'),
                    'sixes': batsman.get('six_x'),
                    'strike_rate': batsman.get('rate')
                }

                if batsman.get('catch_stump_player_id') or batsman.get('runout_by_id') or batsman.get('batsmanout_id') \
                        or batsman.get('bowling_player_id'):
                    data['dismissed'] = True

                self.dao.upsert_batting_scores(tournament_id, match_id, batsman_id, data)

                if batsman.get('catch_stump_player_id'):
                    self.dao.upsert_fielding_scores(tournament_id, match_id, batsman_id)

                if batsman.get('runout_by_id'):
                    self.dao.upsert_fielding_scores(tournament_id, match_id, batsman_id, 'run-out')

        if bowling_data:
            for bowler in bowling_data:
                bowler_id = bowler.get('player_id')

                data = {
                    'wickets': bowler.get('wickets'),
                    'balls_bowled': bowler.get('overs') * 6 if bowler.get('overs') else 0,
                    'dots': 0,
                    'maidens': bowler.get('medians'),
                    'economy': bowler.get('rate'),
                    'runs_conceded': bowler.get('runs')
                }

                self.dao.upsert_bowling_scores(tournament_id, match_id, bowler_id, data)

        return
