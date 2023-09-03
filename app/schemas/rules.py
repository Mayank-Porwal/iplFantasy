from marshmallow import Schema, fields


class GlobalRulesResponse(Schema):
    id = fields.Int(required=True)
    type = fields.Str(required=True)
    rule = fields.Str(required=True)
    value = fields.Int(required=True)


class RuleDataSchema(Schema):
    id = fields.Int(required=True)
    value = fields.Int(required=True)


class SetLeagueRulesRequestSchema(Schema):
    league_id = fields.Int(required=True)
    rule_data = fields.List(fields.Nested(RuleDataSchema), required=True)  # type: ignore
