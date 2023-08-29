from app.models.match import Match
from app.utils.match import MatchStatus


class MatchDAO:
    @staticmethod
    def get_current_match_id_by_status(status: str = 'NOT_STARTED') -> Match | None:
        match: Match = Match.query.filter_by(status=MatchStatus[status.upper()].value)\
            .order_by(Match.schedule.asc())\
            .limit(1).first()

        return match if match else None

    @staticmethod
    def get_match_by_id(fixture_id: int) -> Match | dict:
        match: Match = Match.query.filter_by(id=fixture_id).first()
        return match if match else {}

    @staticmethod
    def create_fixture(fixture_data: dict) -> None:
        fixture = Match(**fixture_data)
        fixture.save()
