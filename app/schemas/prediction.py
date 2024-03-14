from marshmallow import Schema, fields


class PredictionRequestSchema(Schema):
    predicted_team = fields.Str(allow_none=True)
    league_id = fields.Int(required=True)
    team_id = fields.Int(required=True)


class PredictionGetSchema(Schema):
    league_id = fields.Int(required=True)
    team_id = fields.Int(required=True)


class PredictionGetResponse(Schema):
    name = fields.Str(allow_none=True)
