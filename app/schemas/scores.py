from marshmallow import Schema, fields


class LastFiveMatchesStatsRequestSchema(Schema):
    player_id = fields.Int(required=True)
    n = fields.Int(required=True)


class LastFiveMatchesStatsResponseSchema(Schema):
    opponent = fields.Str(required=True)
    runs_scored = fields.Int(required=True)
    balls_faced = fields.Int(required=True)
    strike_rate = fields.Float(required=True)
    wickets = fields.Int(required=True)
    economy = fields.Float(required=True)
    overs = fields.Str(required=True)
    runs_conceded = fields.Int(required=True)
    catches = fields.Int(required=True)
    stumping = fields.Int(required=True)
    run_outs = fields.Int(required=True)
