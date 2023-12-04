from marshmallow import Schema, fields, ValidationError


class CreateLeagueRequestSchema(Schema):
    league_name = fields.Str(required=True)
    type = fields.Str(required=True)
    team_name = fields.Str(required=True)


class CreateLeagueResponseSchema(Schema):
    message = fields.Str(required=True)
    league_id = fields.Int(required=True)
    team_id = fields.Int(required=True)
    team_name = fields.Str(required=True)


class LeagueGetSchema(Schema):
    league_id = fields.Int(required=True)


class JoinLeagueSchema(Schema):
    team_name = fields.Str(required=True)
    code = fields.Str()
    league_id = fields.Int()


class TransferLeagueOwnershipSchema(Schema):
    league_id = fields.Int(required=True)
    new_owner = fields.Str(required=True)


class LeaguePlayersResponse(Schema):
    rank = fields.Int(required=True)
    team_id = fields.Int(required=True)
    team_name = fields.Str(required=True)
    team_owner = fields.Str(required=True)
    remaining_subs = fields.Int(required=True)
    points = fields.Float(required=True)


class LeagueGetResponse(Schema):
    league_id = fields.Int(required=True)
    league_name = fields.Str(required=True)
    owner = fields.Int(required=True)
    code = fields.Str(required=True)
    league_players = fields.List(fields.Nested(LeaguePlayersResponse), required=True)  # type: ignore


class MyLeaguesQuerySchema(Schema):
    page = fields.Int(required=True)
    size = fields.Int(required=True)


class FilterDataValueField(fields.Field):
    def _deserialize(self, value, attr, data, **kwargs):
        if isinstance(value, str) or isinstance(value, bool):
            return value
        else:
            raise ValidationError('value should be of type str or boolean')


class MyLeaguesFilterDataSchema(Schema):
    field = fields.Str(required=True)
    operator = fields.Str(required=True)
    value = FilterDataValueField(required=True)


class MyLeaguesPostSchema(Schema):
    filter_data = fields.List(fields.Nested(MyLeaguesFilterDataSchema))  # type: ignore


class MyLeaguesDataResponseSchema(Schema):
    active = fields.Bool(required=True)
    league_id = fields.Int(required=True)
    league_name = fields.Str(required=True)
    type = fields.Str(required=True)
    team_name = fields.Str(required=True)
    rank = fields.Int(required=True)
    owner = fields.Bool(required=True)
    team_id = fields.Int(required=True)
    remaining_subs = fields.Int(required=True)
    points = fields.Float(required=True)


class MyLeaguesResponseSchema(Schema):
    data = fields.List(fields.Nested(MyLeaguesDataResponseSchema), required=True)  # type: ignore
    total = fields.Int(required=True)
    total_pages = fields.Int(required=True)
    page = fields.Int(required=True)
    size = fields.Int(required=True)


class DeleteLeagueRequestSchema(Schema):
    league_id = fields.Int(required=True)


class PublicLeaguesDataResponseSchema(Schema):
    active = fields.Bool(required=True)
    league_id = fields.Int(required=True)
    league_name = fields.Str(required=True)
    type = fields.Str(required=True)
    owner_id = fields.Int(required=True)
    owner_first_name = fields.Str(required=True)
    owner_last_name = fields.Str(required=True)


class PublicLeaguesResponseSchema(Schema):
    data = fields.List(fields.Nested(PublicLeaguesDataResponseSchema), required=True)  # type: ignore
    total = fields.Int(required=True)
    total_pages = fields.Int(required=True)
    page = fields.Int(required=True)
    size = fields.Int(required=True)
