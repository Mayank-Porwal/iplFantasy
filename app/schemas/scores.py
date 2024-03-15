from marshmallow import Schema, fields


class FantasyPointsRequestResponse(Schema):
    league_id = fields.Int(required=True)
