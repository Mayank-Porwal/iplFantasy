class LastNStatsDTO:
    def __init__(self, **kwargs):
        self.opponent = kwargs.get('opponent', '-')
        self.runs_scored = kwargs.get('runs_scored', 0)
        self.balls_faced = kwargs.get('balls_faced', 0)
        self.strike_rate = kwargs.get('strike_rate', 0.0)
        self.wickets = kwargs.get('wickets', 0)
        self.economy = kwargs.get('economy', 0.0)
        self.overs = kwargs.get('overs', 0)
        self.runs_conceded = kwargs.get('runs_conceded', 0)
        self.catches = kwargs.get('catches', 0)
        self.stumping = kwargs.get('stumping', 0)
        self.run_outs = kwargs.get('run_outs', 0)

    def to_dict(self):
        return self.__dict__
