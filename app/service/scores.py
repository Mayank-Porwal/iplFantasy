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
                    'economy': bowler.get('rate')
                }

                self.dao.upsert_bowling_scores(tournament_id, match_id, bowler_id, data)

        return

    @staticmethod
    def calculate_fantasy_points(league_id: int, tournament_id: int = 1) -> None:
        match: Match = MatchDAO.get_current_match_id_by_status()
        snapshots: list[Snapshot] = SnapshotDAO.get_all_rows_for_current_match(match.id)

        league_rules: list[dict] = LeagueRulesDAO.get_league_rules(league_id)
        league_rule_map = {rule['id']: rule['value'] for rule in league_rules}

        for snapshot in snapshots:
            total_points = 0
            prediction = PredictionDAO.get_predicted_team_for_current_match(match.id,
                                                                            snapshot.user_id,
                                                                            snapshot.team_id,
                                                                            league_id)
            if prediction:
                if match.winner_team_id == prediction:
                    total_points += league_rule_map.get(19, 0)
                else:
                    total_points += league_rule_map.get(20, 0)

            for player in snapshot.team_snapshot:
                score: Scores = ScoresDAO.get_scores_for_a_player(tournament_id, match.id, player['id'])
                batting_points, bowling_points, fielding_points, bonus = 0, 0, 0, 0

                if score.runs_scored == 0 and score.dismissed:  # rule_id = 8
                    batting_points += league_rule_map.get(8, 0)

                if score.runs_scored > 0:  # 115
                    if score.runs_scored >= 25:
                        batting_points += league_rule_map.get(4, 0)
                    if score.runs_scored >= 50:
                        batting_points += league_rule_map.get(5, 0)
                    if score.runs_scored >= 75:
                        batting_points += league_rule_map.get(6, 0)
                    if score.runs_scored >= 100:
                        batting_points += league_rule_map.get(7, 0)

                    runs = score.runs_scored + (score.runs_scored - score.balls_faced)

                    batting_points += runs * league_rule_map.get(1, 0)
                    batting_points += score.fours * league_rule_map.get(3, 0)
                    batting_points += score.sixes * league_rule_map.get(2, 0)

                if score.balls_bowled > 0:
                    bowling_points += score.maidens * league_rule_map.get(13, 0)
                    bowling_points += score.wickets * league_rule_map.get(9, 0)

                    if score.wickets >= 3:  # 6
                        bowling_points += league_rule_map.get(10, 0)
                    if score.wickets >= 4:
                        bowling_points += league_rule_map.get(11, 0)
                    if score.wickets >= 5:
                        bowling_points += league_rule_map.get(12, 0)

                    bowling_points += score.dots * league_rule_map.get(14, 0)

                if score.catches > 0:
                    fielding_points += score.catches * league_rule_map.get(15, 0)
                if score.run_outs > 0:
                    fielding_points += score.run_outs * league_rule_map.get(16, 0)

                if score.man_of_the_match:
                    bonus += league_rule_map.get(18, 0)

                total_points += batting_points + bowling_points + fielding_points + bonus

            snapshot.match_points = total_points
            snapshot.cumulative_points += snapshot.match_points
            snapshot.save()
