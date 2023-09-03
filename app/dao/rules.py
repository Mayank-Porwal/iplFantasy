from app.models.rules import Rules
from app.models.league_rules import LeagueRules


class GlobalRulesDAO:
    @staticmethod
    def get_all_rules() -> list[Rules]:
        rules: list = Rules.query.all()
        return rules if rules else []


class LeagueRulesDAO:
    @staticmethod
    def create_league_rules(league_id: int, rule_id: int, value: int) -> None:
        league_rule: LeagueRules = LeagueRules(league_id=league_id, rule_id=rule_id, value=value)
        league_rule.save()
