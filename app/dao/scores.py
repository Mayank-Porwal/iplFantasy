import sqlalchemy.orm

from db import db
from app.models.scores import Scores
from app.models.teams import UserTeam
from app.models.users import User
from app.models.snapshot import Snapshot
from app.dao.users import UserDAO
from app.utils.common_utils import generate_uuid
from app.utils.rules import RuleType
from sqlalchemy import text


class ScoresDAO:
    def __init__(self):
        self.user_dao = UserDAO

    @staticmethod
    def upsert_batting_scores(tournament_id: int, match_id: int, player_id: int, data: dict) -> None:
        row: Scores = (Scores.query.filter_by(tournament_id=tournament_id, match_id=match_id, player_id=player_id).
                       first())
        if not row:
            row = Scores(tournament_id=tournament_id, match_id=match_id, player_id=player_id)

        row.runs_scored += data.get('runs_scored')
        row.balls_faced += data.get('balls_faced')
        row.sixes += data.get('sixes')
        row.fours += data.get('fours')
        row.strike_rate += data.get('strike_rate')
        row.dismissed = data.get('dismissed') if data.get('dismissed') else False

        row.save()

    @staticmethod
    def upsert_fielding_scores(tournament_id: int, match_id: int, player_id: int, flag='catch') -> None:
        row: Scores = Scores.query.filter_by(tournament_id=tournament_id, match_id=match_id,
                                             player_id=player_id).first()
        if not row:
            row = Scores(tournament_id=tournament_id, match_id=match_id, player_id=player_id)

        if flag == 'catch':
            row.catches += 1
        else:
            row.run_outs += 1

        row.save()

    @staticmethod
    def upsert_man_of_the_match_score(tournament_id: int, match_id: int, player_id: int) -> None:
        row: Scores = Scores.query.filter_by(tournament_id=tournament_id, match_id=match_id,
                                             player_id=player_id).first()
        if not row:
            row = Scores(tournament_id=tournament_id, match_id=match_id, player_id=player_id)

        row.man_of_the_match = True
        row.save()

    @staticmethod
    def upsert_bowling_scores(tournament_id: int, match_id: int, player_id: int, data: dict) -> None:
        row: Scores = Scores.query.filter_by(tournament_id=tournament_id, match_id=match_id,
                                             player_id=player_id).first()
        if not row:
            row = Scores(tournament_id=tournament_id, match_id=match_id, player_id=player_id)

        row.wickets += data.get('wickets')
        row.balls_bowled += data.get('balls_bowled')
        row.dots += 0
        row.maidens += data.get('maidens')
        row.economy = data.get('economy')
        row.runs_conceded += data.get('runs_conceded')

        row.save()

    @staticmethod
    def get_scores_for_a_player(tournament_id: int, match_id: int, player_id: int) -> Scores | None:
        row = Scores.query.filter_by(tournament_id=tournament_id, match_id=match_id, player_id=player_id).first()
        return row if row else {}
