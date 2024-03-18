from marshmallow import Schema, fields


class MatchLeaderBoardRequestSchema(Schema):
    league_id = fields.Int(required=True)


class MatchLeaderBoardDataSchema(Schema):
    id = fields.Int(required=True)
    name = fields.Str(required=True)
    points = fields.Str(required=True)


class MatchLeaderBoardResponseSchema(Schema):
    team_id = fields.Int(required=True)
    data = fields.List(fields.Nested(MatchLeaderBoardDataSchema))  # type: ignore
