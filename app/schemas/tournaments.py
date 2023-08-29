from marshmallow import Schema, fields


class CreateTournamentRequestSchema(Schema):
    name = fields.Str(required=True)
    season = fields.Str(required=True)
    type = fields.Str(required=True)
    start_date = fields.DateTime(required=True)
    end_date = fields.DateTime(required=True)
    teams = fields.List(fields.Int(required=True))
