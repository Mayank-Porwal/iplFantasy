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

    @staticmethod
    def update_league_rules(league_id: int, rule_id: int, value: int, is_active: bool) -> None:
        league_rule: LeagueRules = LeagueRules.query.filter_by(league_id=league_id, rule_id=rule_id).first()
        if league_rule.value != value:
            league_rule.value = value

        if league_rule.is_active != is_active:
            league_rule.is_active = is_active

        league_rule.save()

    @staticmethod
    def get_league_rules(league_id: int) -> list[dict]:
        result: list = (db.session.query(LeagueRules, Rules)
                        .join(Rules, Rules.id == LeagueRules.rule_id)
                        .filter(LeagueRules.league_id == league_id)
                        .order_by(Rules.id.asc()))
        return result

    @staticmethod
    def get_league_rules_map(league_id: int) -> dict | None:
        league_rules = LeagueRulesDAO.get_league_rules(league_id)
        return {i[0].rule_id: i[0].value for i in league_rules if i[0].is_active}
