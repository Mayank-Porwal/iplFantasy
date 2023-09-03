from flask_smorest import abort
from app.models.rules import Rules
from app.models.leagues import League
from app.models.users import User
from app.dao.rules import GlobalRulesDAO, LeagueRulesDAO
from app.dao.leagues import LeagueDAO
from app.dao.users import UserDAO
from app.utils.rules import RuleType, BattingRules, BowlingRules, FieldingRules, AwardRules, RulesUtil


class GlobalRulesService:
    def __init__(self):
        self.dao = GlobalRulesDAO

    @staticmethod
    def create_global_fantasy_rules() -> dict[str, str]:
        batting_rules: list[dict] = BattingRules.get_all_batting_rules()
        bowling_rules: list[dict] = BowlingRules.get_all_bowling_rules()
        fielding_rules: list[dict] = FieldingRules.get_all_fielding_rules()
        award_rules: list[dict] = AwardRules.get_all_award_rules()

        try:
            for row in batting_rules:
                rule = Rules(type=RuleType.batting.value, rule=row['label'], value=row['value'])
                rule.save()

            for row in bowling_rules:
                rule = Rules(type=RuleType.bowling.value, rule=row['label'], value=row['value'])
                rule.save()

            for row in fielding_rules:
                rule = Rules(type=RuleType.fielding.value, rule=row['label'], value=row['value'])
                rule.save()

            for row in award_rules:
                rule = Rules(type=RuleType.awards.value, rule=row['label'], value=row['value'])
                rule.save()
            return {'message': 'Added global rules successfully'}

        except Exception as e:
            return {'message': f'Failed with exception: {e}'}

    def get_all_global_rules(self):
        rules = self.dao.get_all_rules()

        output = []
        for rule in rules:
            row = RulesUtil.convert_object_to_dict(rule)
            output.append(row)

        return output


class LeagueRulesService:
    def __init__(self):
        self.dao = LeagueRulesDAO

    def create_league_rules(self, league_id: int, email: str, rule_data: list[dict[str, int]]) -> dict:
        league: League = LeagueDAO.get_league_by_id(league_id)
        if not league:
            abort(404, message='League not found')

        user: User = UserDAO.get_user_by_email(email)
        if not user:
            abort(404, message='User not found')

        if user.id != league.owner:
            abort(403, message='Only owner can choose rules for the league')

        for rule in rule_data:
            self.dao.create_league_rules(league_id, rule['id'], rule['value'])

        return {'message': 'Created league rules successfully'}
