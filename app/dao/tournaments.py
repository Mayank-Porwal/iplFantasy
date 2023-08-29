from app.models.tournament import Tournament


class TournamentDAO:
    @staticmethod
    def get_tournament_by_id(tournament_id: int, active: bool = True) -> Tournament:
        tournament: Tournament = Tournament.query.filter_by(id=tournament_id, is_active=active).first()
        return tournament if tournament_id else {}

    @staticmethod
    def get_tournament_by_name(name: str, active: bool = True) -> Tournament:
        tournament: Tournament = Tournament.query.filter_by(name=name, is_active=active).first()
        return tournament if tournament else {}

    @staticmethod
    def get_tournament(active: bool = True) -> Tournament:
        tournament: Tournament = Tournament.query.filter_by(is_active=active).first()
        return tournament if tournament else {}

    @staticmethod
    def create_tournament(data: dict) -> None:
        tournament = Tournament(**data)
        tournament.save()
