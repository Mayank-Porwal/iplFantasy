from flask_smorest import Blueprint
from flask.views import MethodView
from flask_cors import cross_origin
from flask_jwt_extended import jwt_required
from app.schemas.util import PostResponseSuccessSchema
from app.utils.common_utils import fetch_user_from_jwt
from app.schemas.rules import GlobalRulesResponse, SetLeagueRulesRequestSchema
from app.service.rules import GlobalRulesService, LeagueRulesService

blp = Blueprint('Global_Rules', __name__, description='Global Rules related endpoints')
global_rules_service = GlobalRulesService()
league_rules_service = LeagueRulesService()


@blp.route('/global-rules')
class GlobalRules(MethodView):
    @cross_origin()
    @blp.response(201, PostResponseSuccessSchema)
    def post(self):
        return global_rules_service.create_global_fantasy_rules()

    @cross_origin()
    @jwt_required()
    @blp.response(200, GlobalRulesResponse(many=True))
    def get(self):
        return global_rules_service.get_all_global_rules()


@blp.route('/league-rules')
class LeagueRules(MethodView):
    @cross_origin()
    @jwt_required()
    @blp.arguments(SetLeagueRulesRequestSchema)
    @blp.response(201, PostResponseSuccessSchema)
    def post(self, payload):
        league_id = payload.get('league_id')
        rule_data = payload.get('rule_data')
        email = fetch_user_from_jwt()

        return league_rules_service.create_league_rules(league_id, email, rule_data)
