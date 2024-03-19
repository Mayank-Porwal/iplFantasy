from flask_smorest import Blueprint
from flask.views import MethodView
from flask_cors import cross_origin
from app.schemas.snapshot import SubmitTeamRequestSchema
from app.schemas.util import PostResponseSuccessSchema
from app.service.snapshot import SnapshotService

blp = Blueprint('Snapshot', __name__, description='Team snapshot related endpoints')
service = SnapshotService()


@blp.route('/submit-all-teams-in-league')
class SubmitTeam(MethodView):
    @cross_origin()
    @blp.arguments(SubmitTeamRequestSchema)
    @blp.response(201, PostResponseSuccessSchema)
    def put(self, payload: dict):
        match_id = payload.get('match_id')
        league_id = payload.get('league_id')

        return service.submit_all_teams_for_league(match_id, league_id)
