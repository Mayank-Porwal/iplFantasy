from flask_smorest import abort
from app.dao.tournaments import TournamentDAO


class TournamentService:
    def __init__(self) -> None:
        self.dao = TournamentDAO

    def create_tournament(self, dto) -> dict:
        tournament = self.dao.get_tournament_by_name(dto['name'])
        if tournament:
            abort(409, message=f"{tournament.name} already exists.")

        self.dao.create_tournament(dto)
        return {'message': 'Tournament created successfully'}
