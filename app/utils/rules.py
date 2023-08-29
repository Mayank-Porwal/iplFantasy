class RuleType:
    BATTING = 'batting'
    BOWLING = 'bowling'
    FIELDING = 'fielding'
    AWARDS = 'awards'


class BattingRules:
    RUN = {'label': 'Run points', 'value': 1}
    SIX_RUN_BONUS = {'label': '6-runs bonus', 'value': 2}
    FOUR_RUN_BONUS = {'label': '4-runs bonus', 'value': 1}
    TWENTY_FIVE_RUN_BONUS = {'label': '25 runs milestone', 'value': 10}
    FIFTY_RUN_BONUS = {'label': '50 runs milestone', 'value': 20}
    SEVENTY_FIVE_RUN_BONUS = {'label': '75 runs milestone', 'value': 25}
    CENTURY_BONUS = {'label': '100 runs milestone', 'value': 40}
    DUCK = {'label': 'Dismissed on duck', 'value': -15}

    def batting_rules_points(self,
                             run: int = 0,
                             six: int = 0,
                             four: int = 0,
                             twenty_five: int = 0,
                             fifty: int = 0,
                             seventy_five: int = 0,
                             century: int = 0,
                             duck: int = 0
                             ) -> list[dict]:
        return [
            {
                'type': RuleType.BATTING,
                'rule': self.RUN['label'],
                'default': self.RUN['value'],
                'new_value': run if run else self.RUN['value']
            },
            {
                'type': RuleType.BATTING,
                'rule': self.SIX_RUN_BONUS['label'],
                'default': self.SIX_RUN_BONUS['value'],
                'new_value': six if six else self.SIX_RUN_BONUS['value']
            },
            {
                'type': RuleType.BATTING,
                'rule': self.FOUR_RUN_BONUS['label'],
                'default': self.FOUR_RUN_BONUS['value'],
                'new_value': four if four else self.FOUR_RUN_BONUS['value']
            },
            {
                'type': RuleType.BATTING,
                'rule': self.TWENTY_FIVE_RUN_BONUS['label'],
                'default': self.TWENTY_FIVE_RUN_BONUS['value'],
                'new_value': twenty_five if twenty_five else self.TWENTY_FIVE_RUN_BONUS['value']
            },
            {
                'type': RuleType.BATTING,
                'rule': self.FIFTY_RUN_BONUS['label'],
                'default': self.FIFTY_RUN_BONUS['value'],
                'new_value': fifty if fifty else self.FIFTY_RUN_BONUS['value']
            },
            {
                'type': RuleType.BATTING,
                'rule': self.SEVENTY_FIVE_RUN_BONUS['label'],
                'default': self.SEVENTY_FIVE_RUN_BONUS['value'],
                'new_value': seventy_five if seventy_five else self.SEVENTY_FIVE_RUN_BONUS['value']
            },
            {
                'type': RuleType.BATTING,
                'rule': self.CENTURY_BONUS['label'],
                'default': self.CENTURY_BONUS['value'],
                'new_value': century if century else self.CENTURY_BONUS['value']
            },
            {
                'type': RuleType.BATTING,
                'rule': self.DUCK['label'],
                'default': self.DUCK['value'],
                'new_value': duck if duck else self.DUCK['value']
            }
        ]


class BowlingRules:
    WICKET = {'label': 'Wicket points', 'value': 20}
    THREE_WICKET_BONUS = {'label': '3-wickets bonus', 'value': 10}
    FOUR_WICKET_BONUS = {'label': '4-wickets bonus', 'value': 15}
    FIVE_WICKET_BONUS = {'label': '5-wickets bonus', 'value': 25}
    MAIDEN_BONUS = {'label': 'Maiden bonus', 'value': 25}
    DOT_BALL_BONUS = {'label': 'Dot-ball bonus', 'value': 1}

    def bowling_rules_points(self,
                             wicket: int = 0,
                             three: int = 0,
                             four: int = 0,
                             five: int = 0,
                             maiden: int = 0,
                             dot: int = 0
                             ) -> list[dict]:
        return [
            {
                'type': RuleType.BOWLING,
                'rule': self.WICKET['label'],
                'default': self.WICKET['value'],
                'new_value': wicket if wicket else self.WICKET['value']
            },
            {
                'type': RuleType.BOWLING,
                'rule': self.THREE_WICKET_BONUS['label'],
                'default': self.THREE_WICKET_BONUS['value'],
                'new_value': three if three else self.THREE_WICKET_BONUS['value']
            },
            {
                'type': RuleType.BOWLING,
                'rule': self.FOUR_WICKET_BONUS['label'],
                'default': self.FOUR_WICKET_BONUS['value'],
                'new_value': four if four else self.FOUR_WICKET_BONUS['value']
            },
            {
                'type': RuleType.BOWLING,
                'rule': self.FIVE_WICKET_BONUS['label'],
                'default': self.FIVE_WICKET_BONUS['value'],
                'new_value': five if five else self.FIVE_WICKET_BONUS['value']
            },
            {
                'type': RuleType.BOWLING,
                'rule': self.MAIDEN_BONUS['label'],
                'default': self.MAIDEN_BONUS['value'],
                'new_value': maiden if maiden else self.MAIDEN_BONUS['value']
            },
            {
                'type': RuleType.BOWLING,
                'rule': self.DOT_BALL_BONUS['label'],
                'default': self.DOT_BALL_BONUS['value'],
                'new_value': dot if dot else self.DOT_BALL_BONUS['value']
            }
        ]


class FieldingRules:
    CATCH_BONUS = {'label': 'Catch bonus', 'value': 10}
    RUN_OUT_BONUS = {'label': 'Run-Out bonus', 'value': 15}
    STUMPING_BONUS = {'label': 'Stumping bonus', 'value': 15}

    def fielding_rules_points(self,
                              catch: int = 0,
                              run_out: int = 0,
                              stumping: int = 0
                              ) -> list[dict]:
        return [
            {
                'type': RuleType.FIELDING,
                'rule': self.CATCH_BONUS['label'],
                'default': self.CATCH_BONUS['value'],
                'new_value': catch if catch else self.CATCH_BONUS['value']
            },
            {
                'type': RuleType.FIELDING,
                'rule': self.RUN_OUT_BONUS['label'],
                'default': self.RUN_OUT_BONUS['value'],
                'new_value': run_out if run_out else self.RUN_OUT_BONUS['value']
            },
            {
                'type': RuleType.FIELDING,
                'rule': self.STUMPING_BONUS['label'],
                'default': self.STUMPING_BONUS['value'],
                'new_value': stumping if stumping else self.STUMPING_BONUS['value']
            }
        ]


class AwardRules:
    MAN_OF_THE_MATCH_BONUS = {'label': 'Man of the match bonus', 'value': 50}
    PREDICTION_BONUS = {'label': 'Prediction Bonus', 'value': 50}

    def award_rules_points(self,
                           mom: int = 0,
                           prediction: int = 0
                           ) -> list[dict]:
        return [
            {
                'type': RuleType.AWARDS,
                'rule': self.MAN_OF_THE_MATCH_BONUS['label'],
                'default': self.MAN_OF_THE_MATCH_BONUS['value'],
                'new_value': mom if mom else self.MAN_OF_THE_MATCH_BONUS['value']
            },
            {
                'type': RuleType.AWARDS,
                'rule': self.PREDICTION_BONUS['label'],
                'default': self.PREDICTION_BONUS['value'],
                'new_value': prediction if prediction else self.PREDICTION_BONUS['value']
            }
        ]


class Rule:
    def __init__(self):
        self.rule_type = RuleType()
        self.batting_rules = BattingRules()
        self.bowling_rules = BowlingRules()
        self.fielding_rules = FieldingRules()
        self.award_rules = AwardRules()

    def get_all_rules(self) -> list[dict]:
        all_rules: list[dict] = self.batting_rules.batting_rules_points()
        all_rules.extend(self.bowling_rules.bowling_rules_points())
        all_rules.extend(self.fielding_rules.fielding_rules_points())
        all_rules.extend(self.award_rules.award_rules_points())

        return all_rules
