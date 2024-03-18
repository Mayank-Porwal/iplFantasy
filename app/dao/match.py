from app.models.match import Match
from app.utils.match import MatchStatus


class MatchDAO:
    @staticmethod
    def get_current_match_id_by_status(status: str = 'NS') -> Match | None:
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

    @staticmethod
    def get_upcoming_matches_by_status(status: str = 'NS') -> list[Match] | None:
        match: list[Match] = Match.query.filter_by(status=MatchStatus[status.upper()].value) \
            .order_by(Match.schedule.asc()) \
            .limit(4).all()

        return match if match else []

    @staticmethod
    def get_previous_completed_match(status: str = 'FINISHED') -> Match | None:
        match: list[Match] = (Match.query.filter_by(status=MatchStatus[status.upper()].value)
                              .order_by(Match.schedule.asc()).all())
        return match[-2] if match else {}

    @staticmethod
    def get_previous_completed_matches(status: str = 'FINISHED') -> list[Match] | None:
        match: list[Match] = (Match.query.filter_by(status=MatchStatus[status.upper()].value)
                              .order_by(Match.schedule.desc()).all())
        return match if match else []

