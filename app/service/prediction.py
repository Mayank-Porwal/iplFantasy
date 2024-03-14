from flask_smorest import abort
from app.dao.prediction import PredictionDAO
from app.dao.users import UserDAO
from app.dao.ipl_teams import IplTeamsDAO
from app.dao.teams import TeamDAO
from app.dao.leagues import LeagueDAO
from app.dao.match import MatchDAO
from app.models.users import User
from app.models.teams import UserTeam
from app.models.leagues import League
from app.models.match import Match


class PredictionService:
    def __init__(self) -> None:
        self.dao = PredictionDAO

    def set_prediction(self, email: str, prediction: str, league_id: int, team_id: int) -> dict:
        user: User = UserDAO.get_user_by_email(email)
        if not user:
            abort(403, message=f'User with email: {email} does not exist')

        team: UserTeam = TeamDAO.get_team_by_id(team_id)
        if not team:
            abort(403, message=f'Team: {team.name} does not exist')

        league: League = LeagueDAO.get_league_by_id(league_id)
        if not league:
            abort(403, message=f'League: {league.name} does not exist')

        match: Match = MatchDAO.get_current_match_id_by_status()
        if not match:
            abort(403, message=f'No current match available')

        dto = {
                    'match_id': match.id,
                    'league_id': league_id,
                    'user_id': user.id,
                    'team_id': team_id
                }

        if prediction:
            predicted_team_id = IplTeamsDAO.get_id_from_team_name(prediction)
            dto['prediction'] = predicted_team_id
            message = 'Prediction successfully saved'
        else:
            dto['prediction'] = None
            message = 'User did not predict'

        self.dao.set_prediction(dto)

        return {'message': message}

    def get_prediction_for_current_match(self, email: str, league_id: int, team_id: int) -> dict | None:
        user: User = UserDAO.get_user_by_email(email)
        if not user:
            abort(403, message=f'User with email: {email} does not exist')

        team: UserTeam = TeamDAO.get_team_by_id(team_id)
        if not team:
            abort(403, message=f'Team: {team.name} does not exist')

        league: League = LeagueDAO.get_league_by_id(league_id)
        if not league:
            abort(403, message=f'League: {league.name} does not exist')

        match: Match = MatchDAO.get_current_match_id_by_status()
        if not match:
            abort(403, message=f'No current match available')

        predicted_team_id = self.dao.get_predicted_team_for_current_match(match.id, user.id, team_id, league_id)
        if predicted_team_id:
            predicted_team = IplTeamsDAO.get_ipl_team_by_id(predicted_team_id)
            return {'name': predicted_team.code}
        return
