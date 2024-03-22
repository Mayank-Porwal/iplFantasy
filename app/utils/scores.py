from app.dao.rules import GlobalRulesDAO
from app.models.scores import Scores


global_rules = GlobalRulesDAO.get_all_rules()
global_rules_map = {rule.rule: rule.id for rule in global_rules}


def calculate_batting_fantasy_score(score: Scores, league_rules_map: dict) -> float:
    points = 0
    if score.runs_scored == 0 and score.dismissed:  # rule_id = 8
        points += league_rules_map.get(global_rules_map['Dismissed on duck'], 0)

    if score.runs_scored > 0:  # 115
        if score.runs_scored >= 25:
            points += league_rules_map.get(global_rules_map['25 runs milestone'], 0)
        if score.runs_scored >= 50:
            points += league_rules_map.get(global_rules_map['50 runs milestone'], 0)
        if score.runs_scored >= 75:
            points += league_rules_map.get(global_rules_map['75 runs milestone'], 0)
        if score.runs_scored >= 100:
            points += league_rules_map.get(global_rules_map['100 runs milestone'], 0)

        points += (score.runs_scored - score.balls_faced) * 2  # strike-rate

        points += score.runs_scored * league_rules_map.get(global_rules_map['Run points'], 0)
        points += score.fours * league_rules_map.get(global_rules_map['4-runs bonus'], 0)
        points += score.sixes * league_rules_map.get(global_rules_map['6-runs bonus'], 0)

    return points


def calculate_bowling_fantasy_score(score: Scores, league_rules_map: dict) -> float:
    points = 0
    if score.balls_bowled > 0:
        points += score.maidens * league_rules_map.get(global_rules_map['Maiden bonus'], 0)
        points += score.wickets * league_rules_map.get(global_rules_map['Wicket points'], 0)

        if score.wickets >= 3:  # 6
            points += league_rules_map.get(global_rules_map['3-wickets bonus'], 0)
        if score.wickets >= 4:
            points += league_rules_map.get(global_rules_map['4-wickets bonus'], 0)
        if score.wickets >= 5:
            points += league_rules_map.get(global_rules_map['5-wickets bonus'], 0)

        points += score.dots * league_rules_map.get(global_rules_map['Dot-ball bonus'], 0)
        points += ((score.balls_bowled * 1.5) - score.runs_conceded) * 2  # economy

    return points


def calculate_fielding_fantasy_score(score: Scores, league_rules_map: dict) -> float:
    points = 0
    if score.catches > 0:
        points += score.catches * league_rules_map.get(global_rules_map['Catch bonus'], 0)
    if score.run_outs > 0:
        points += score.run_outs * league_rules_map.get(global_rules_map['Run-Out bonus'], 0)

    return points


def calculate_award_fantasy_score(score: Scores, league_rules_map: dict) -> float:
    points = 0
    if score.man_of_the_match:
        points += league_rules_map.get(global_rules_map['Man of the match bonus'], 0)

    return points


def total_fantasy_points_of_player(score: Scores, league_rules_map: dict) -> float:
    batting_points = calculate_batting_fantasy_score(score, league_rules_map)
    bowling_points = calculate_bowling_fantasy_score(score, league_rules_map)
    fielding_points = calculate_fielding_fantasy_score(score, league_rules_map)
    award_points = calculate_award_fantasy_score(score, league_rules_map)

    return batting_points + bowling_points + fielding_points + award_points


def calculate_overs_from_balls(balls: int) -> str:
    if balls > 0:
        if balls % 6 == 0:
            return str(balls // 6)
        else:
            return f'{(balls // 6)}.{balls % 6}'

    return '0'


def calculate_balls_from_overs(overs: int) -> int:
    overs = str(overs)
    if overs:
        if '.' in overs:
            over, balls = overs.split('.')
            return (int(over) * 6) + int(balls)
        else:
            return int(overs) * 6

    return 0
