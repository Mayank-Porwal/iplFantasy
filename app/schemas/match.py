from marshmallow import Schema, fields


class CompletedMatchesResponseSchema(Schema):
    number = fields.Int(required=True)
    match = fields.Str(required=True)
    match_id = fields.Int(required=True)
