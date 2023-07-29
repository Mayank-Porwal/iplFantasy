from marshmallow import Schema, fields


class GetTeamResponseSchema(Schema):
    id = fields.Int(required=True)
    name = fields.Str(required=True)
    team = fields.Str(required=True)
    category = fields.Str(required=True)
    cap = fields.Int(required=True)
    img = fields.Str(required=True)
    captain = fields.Bool(default=False)
    vice_captain = fields.Bool(default=False)


class TeamPlayersSchema(Schema):
    id = fields.Int(required=True)
    captain = fields.Bool(required=True)
    vice_captain = fields.Bool(required=True)


class TeamSchema(Schema):
    team_name = fields.Str(required=True)
    email = fields.Str(required=True)
    players = fields.List(fields.Nested(TeamPlayersSchema))


class MyTeamsRequestSchema(Schema):
    email = fields.Str(required=True)


class TeamResponseSchema(Schema):
    team_name = fields.Str(required=True, attribute='name')
    players = fields.List(fields.Nested(TeamPlayersSchema))


class RandomTeamSchema(Schema):
    team_name = fields.Str(required=True)
    email = fields.Str(required=True)

