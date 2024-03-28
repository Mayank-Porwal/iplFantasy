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
    def get_first_match_of_tournament(tournament_id: int) -> Match | None:
        match: Match = (Match.query.filter_by(tournament_id=tournament_id).order_by(Match.schedule.asc()).limit(1).
                        first())
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
        print(f'match: {match}')
        return match[-2] if match else {}

    @staticmethod
    def get_previous_completed_matches(status: str = 'FINISHED') -> list[Match] | None:
        match: list[Match] = (Match.query.filter_by(status=MatchStatus[status.upper()].value)
                              .order_by(Match.schedule.desc()).all())
        return match if match else []

    @staticmethod
    def get_previous_match_of_given_match(current_match_id: int) -> Match | None:
        match: Match = Match.query.filter(Match.id < current_match_id).order_by(Match.schedule.desc()).limit(1).first()

        return match if match else {}

    @staticmethod
    def update_match_status(match: Match, tournament_id: int = 1, flag='completed') -> None:
        if match:
            if match.tournament_id == tournament_id:
                if flag == 'completed':
                    match.status = 3
                else:
                    match.status = 2

                match.save()

    @staticmethod
    def get_recent_completed_match(status: int = 3) -> Match | None:
        match: Match = Match.query.filter_by(status=status).order_by(Match.schedule.desc()).limit(1).first()

        return match if match else None

    @staticmethod
    def update_winner_team_id(match: Match, winner_team_id: int, tournament_id: int = 1) -> None:
        if match:
            if match.tournament_id == tournament_id:
                match.winner_team_id = winner_team_id

                match.save()

    @staticmethod
    def get_next_match_from_current_match(match_id: int) -> Match | None:
        match: Match = Match.query.filter(Match.id > match_id).order_by(Match.schedule.asc()).limit(1).first()

        return match if match else None
