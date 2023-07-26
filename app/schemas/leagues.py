from marshmallow import Schema, fields


class LeagueSchema(Schema):
    league_name = fields.Str(required=True)
    email = fields.Str(required=True)
    type = fields.Str()


class LeagueGetSchema(Schema):
    league_name = fields.Str(required=True)


class JoinLeagueSchema(Schema):
    team_name = fields.Str(required=True)
    code = fields.Str()
    email = fields.Str(required=True)
    type = fields.Str(required=True)
    league_name = fields.Str(required=True)


class TransferLeagueOwnershipSchema(Schema):
    league_name = fields.Str(required=True)
    email = fields.Str(required=True)
    new_owner = fields.Str(required=True)


class LeagueGetResponse(Schema):
    rank = fields.Int(required=True)
    team_name = fields.Str(required=True)
    team_owner = fields.Str(required=True)
    remaining_subs = fields.Int(required=True)
    points = fields.Float(required=True)
