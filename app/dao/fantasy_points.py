from app.models.scores import Scores
from app.models.fantasy_points import FantasyPoints
from app.dao.scores import ScoresDAO
from app.dao.rules import LeagueRulesDAO
from app.utils.scores import total_fantasy_points_of_player


class FantasyPointsDAO:
    @staticmethod
    def save_fantasy_points_per_player_per_league(match_id: int, league_id: int, player_id: int,
                                                  tournament_id: int = 1, captain: bool = False,
                                                  vice_captain: bool = False) -> float:
        scores: Scores = ScoresDAO.get_scores_for_a_player(tournament_id, match_id, player_id)
        league_rules_map = LeagueRulesDAO.get_league_rules_map(league_id)
        points = total_fantasy_points_of_player(scores, league_rules_map)

        if scores:
            row: FantasyPoints = FantasyPoints.query.filter_by(tournament_id=tournament_id, match_id=match_id,
                                                               league_id=league_id, player_id=player_id).first()
            if not row:
                row = FantasyPoints(tournament_id=tournament_id, match_id=match_id, league_id=league_id,
                                    player_id=player_id)
            row.points = points
            row.save()

        if captain:
            return points * 2
        elif vice_captain:
            return points * 1.5
        return points

    @staticmethod
    def get_fantasy_points_of_player_in_league(match_id: int, league_id: int, player_id: int,
                                               tournament_id: int = 1) -> dict:
        row: FantasyPoints = FantasyPoints.query.filter_by(tournament_id=tournament_id, match_id=match_id,
                                                           league_id=league_id, player_id=player_id).first()
        return row if row else {}
