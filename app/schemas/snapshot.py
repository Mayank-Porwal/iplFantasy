from marshmallow import Schema, fields


class SubmitTeamRequestSchema(Schema):
    match_id = fields.Int(required=True)
    league_id = fields.Int(required=True)
