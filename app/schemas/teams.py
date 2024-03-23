from marshmallow import Schema, fields


class GetTeamPlayersResponseSchema(Schema):
    id = fields.Int(required=True)
    name = fields.Str(required=True)
    team = fields.Str(required=True, attribute='ipl_team')
    category = fields.Str(required=True)
    cap = fields.Int(required=True)
    img = fields.Str(required=True, attribute='image_file')
    captain = fields.Bool(default=False)
    vice_captain = fields.Bool(default=False)
    team_img = fields.Str(required=True, attribute='ipl_team_img')


class GetTeamResponseSchema(Schema):
    id = fields.Int(required=True)
    name = fields.Str(required=True)
    substitutions = fields.Int(required=True)
    points = fields.Int(required=True)
    rank = fields.Int(required=True)
    previous_remaining_substitutes = fields.Int(required=True)
    draft_team = fields.List(fields.Nested(GetTeamPlayersResponseSchema))  # type: ignore
    last_submitted_team = fields.List(fields.Nested(GetTeamPlayersResponseSchema))  # type: ignore


class TeamPlayersSchema(Schema):
    id = fields.Int(required=True)
    captain = fields.Bool(required=True)
    vice_captain = fields.Bool(required=True)


class CreateTeamSchema(Schema):
    team_name = fields.Str(required=True)


class GetTeamQuerySchema(Schema):
    team_id = fields.Int(required=True)


class TeamResponseSchema(Schema):
    team_name = fields.Str(required=True, attribute='name')
    players = fields.List(fields.Nested(TeamPlayersSchema))  # type: ignore


class EditTeamRequestSchema(Schema):
    team_id = fields.Int(required=True)
    players = fields.List(fields.Nested(TeamPlayersSchema), required=True)  # type: ignore
    substitutions = fields.Int(required=True)
