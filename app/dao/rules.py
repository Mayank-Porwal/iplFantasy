from db import db
from app.models.rules import Rules
from app.models.league_rules import LeagueRules


class GlobalRulesDAO:
    @staticmethod
    def get_all_rules() -> list[Rules]:
        rules: list = Rules.query.all()
        return rules if rules else []

    @staticmethod
    def get_row_count_of_global_rules() -> int:
        rows: int = Rules.query.count()
        return rows


class LeagueRulesDAO:
    @staticmethod
    def create_league_rules(league_id: int) -> None:
        global_rules: list[Rules] = GlobalRulesDAO.get_all_rules()
        for rule in global_rules:
            league_rule: LeagueRules = LeagueRules(league_id=league_id, rule_id=rule.id, value=rule.value)
            league_rule.save()

    def update_league_rules(league_id: int, rule_id: int, value: int) -> None:
        league_rule: LeagueRules = LeagueRules(league_id=league_id, rule_id=rule_id, value=value)
        league_rule.save()

    @staticmethod
    def get_league_rules(league_id: int) -> list[dict]:
        result: list = (db.session.query(LeagueRules, Rules)
                        .join(Rules, Rules.id == LeagueRules.rule_id)
                        .filter(LeagueRules.league_id == league_id))
        return result
