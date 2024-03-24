import requests
from flask_smorest import abort

from app.dao.scores import ScoresDAO
from app.dao.match import MatchDAO
from app.dto.scores import LastNStatsDTO
from app.models.match import Match
from app.models.scores import Scores
from app.models.ipl_teams import IplTeams
from app.dao.ipl_teams import IplTeamsDAO
from app.dao.players import PlayerDAO
from app.utils.sportsmonk import SportsMonkConstants
from app.utils.scores import calculate_overs_from_balls, calculate_balls_from_overs


class ScoreService:
    def __init__(self) -> None:
        self.dao = ScoresDAO
        self.dto = LastNStatsDTO()

    def upsert_scores_of_players(self, tournament_id: int = 1) -> dict:
        match: Match = MatchDAO.get_recent_completed_match()
        match_id = match.id

        url = f'{SportsMonkConstants.FIXTURE_URL}/{match_id}'
        params = {
            'api_token': SportsMonkConstants.API_KEY,
            'include': 'batting, bowling, manofmatch, manofseries'
        }

        data = requests.get(url=url, params=params).json().get('data')
        if not data:
            abort(404, message='Could not fetch data from 3rd party fixtures endpoint')

        if data['status'] != 'Finished':
            return {'message': 'Match is still not finished. Scores will be updated post that.'}

        # Update winner_team_id in match table
        winner_team_id = data['winner_team_id']
        if winner_team_id:
            MatchDAO.update_winner_team_id(match, winner_team_id)

        batting_data = data.get('batting')
        bowling_data = data.get('bowling')
        man_of_match_player_id = data.get('man_of_match_id')

        if man_of_match_player_id:
            self.dao.upsert_man_of_the_match_score(tournament_id, match_id, man_of_match_player_id)

        if batting_data:
            for batsman in batting_data:
                batsman_id = batsman.get('player_id')
                data = {
                    'runs_scored': batsman.get('score', 0),
                    'balls_faced': batsman.get('ball', 0),
                    'sixes': batsman.get('six_x', 0),
                    'fours': batsman.get('four_x', 0),
                    'strike_rate': batsman.get('rate', 0)
                }

                catch_stump_player_id = batsman.get('catch_stump_player_id')
                run_out_player_id = batsman.get('runout_by_id')

                if catch_stump_player_id or run_out_player_id or batsman.get('batsmanout_id') \
                        or batsman.get('bowling_player_id'):
                    data['dismissed'] = True

                self.dao.upsert_batting_scores(tournament_id, match_id, batsman_id, data)

                if catch_stump_player_id:
                    self.dao.upsert_fielding_scores(tournament_id, match_id, catch_stump_player_id)

                if run_out_player_id:
                    self.dao.upsert_fielding_scores(tournament_id, match_id, run_out_player_id, 'run-out')

        if bowling_data:
            for bowler in bowling_data:
                bowler_id = bowler.get('player_id')

                data = {
                    'wickets': bowler.get('wickets', 0),
                    'balls_bowled': calculate_balls_from_overs(bowler.get('overs')),
                    'dots': 0,
                    'maidens': bowler.get('medians', 0),
                    'economy': bowler.get('rate', 0),
                    'runs_conceded': bowler.get('runs', 0)
                }

                self.dao.upsert_bowling_scores(tournament_id, match_id, bowler_id, data)

        return {'message': 'Scores updated successfully'}

    def get_last_n_stats_for_a_player(self, player_id: int, n: int) -> list[Scores] | None:
        stats = self.dao.get_last_n_stats_for_a_player(player_id, n, tournament_id=1)
        output = []

        if not stats:
            output.append(self.dto.to_dict())
        else:
            for stat in stats:
                match: Match = MatchDAO.get_match_by_id(stat.match_id)
                teams: list = [match.home_team_id, match.away_team_id]
                home_team_id: int = PlayerDAO.get_player_by_id(player_id).ipl_team
                opponent: str = '-'

                for team in teams:
                    if team != home_team_id:
                        ipl_team: IplTeams = IplTeamsDAO.get_ipl_team_by_id(team)
                        opponent = ipl_team.code

                output.append(
                    LastNStatsDTO(
                        opponent=opponent,
                        runs_scored=stat.runs_scored,
                        balls_faced=stat.balls_faced,
                        strike_rate=stat.strike_rate,
                        wickets=stat.wickets,
                        economy=stat.economy,
                        overs=calculate_overs_from_balls(stat.balls_bowled),
                        runs_conceded=stat.runs_conceded,
                        catches=stat.catches,
                        stumping=0,
                        run_outs=stat.run_outs
                    ).to_dict()
                )

        return output
