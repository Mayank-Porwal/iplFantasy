from flask_smorest import Blueprint
from flask.views import MethodView
from flask_cors import cross_origin
from app.schemas.util import PostResponseSuccessSchema
from app.service.ipl_teams import IplTeamsService

blp = Blueprint('Ipl_Teams', __name__, description='Ipl Teams related endpoints')
ipl_teams_service = IplTeamsService()


@blp.route('/ipl-teams')
class IplTeams(MethodView):
    @cross_origin()
    @blp.response(201, PostResponseSuccessSchema)
    def post(self):
        return ipl_teams_service.create_all_teams()
