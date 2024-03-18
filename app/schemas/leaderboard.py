from marshmallow import Schema, fields


class MatchLeaderBoardRequestSchema(Schema):
    match_id = fields.Int(required=True)
    league_id = fields.Int(required=True)


class MatchLeaderBoardDataSchema(Schema):
    id = fields.Int(required=True)
    name = fields.Str(required=True)
    points = fields.Str(required=True)


class MatchLeaderBoardResponseSchema(Schema):
    team_id = fields.Int(required=True)
    team_name = fields.Str(required=True)
    owner = fields.Str(required=True)
    trades = fields.Int(required=True)
    data = fields.List(fields.Nested(MatchLeaderBoardDataSchema))  # type: ignore
