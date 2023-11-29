from marshmallow import Schema, fields


class GlobalRulesResponse(Schema):
    id = fields.Int(required=True)
    type = fields.Str(required=True)
    rule = fields.Str(required=True)
    value = fields.Int(required=True)


class GetLeagueRulesRequestSchema(Schema):
    league_id = fields.Int(required=True)


class GetLeagueRulesResponse(Schema):
    id = fields.Int(required=True)
    rule = fields.Str(required=True)
    type = fields.Str(required=True)
    value = fields.Int(required=True)
    is_active = fields.Bool(required=True)


class SetLeagueRulesRequestSchema(Schema):
    league_id = fields.Int(required=True)
    rule_data = fields.List(fields.Nested(GetLeagueRulesResponse), required=True)  # type: ignore
