from marshmallow import Schema, fields


class LeagueSchema(Schema):
    league_name = fields.Str(required=True)
    user_name = fields.Str(required=True)
    type = fields.Str()


class JoinLeagueSchema(Schema):
    team_name = fields.Str(required=True)
    code = fields.Str()
    user_name = fields.Str(required=True)
    type = fields.Str(required=True)
    league_name = fields.Str(required=True)


class TransferLeagueOwnershipSchema(Schema):
    league_name = fields.Str(required=True)
    user_name = fields.Str(required=True)
    new_owner = fields.Str(required=True)
