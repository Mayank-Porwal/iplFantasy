from marshmallow import Schema, fields


class PlayerResponseSchema(Schema):
    id = fields.Int(required=True)
    name = fields.Str(required=True)
    team = fields.Str(required=True, attribute='ipl_team')
    category = fields.Str(required=True)
    cap = fields.Int(required=True)
    img = fields.Str(required=True, attribute='image_file')
    team_img = fields.Str(required=True, attribute='ipl_team_img')


class LineupResponseSchema(Schema):
    name = fields.Str(required=True)
    image = fields.Str(required=True)
    players = fields.List(fields.Int(allow_none=True))


class PlayingElevenResponseSchema(Schema):
    teamA = fields.Nested(LineupResponseSchema, required=True)  # type: ignore
    teamB = fields.Nested(LineupResponseSchema, required=True)  # type: ignore


class PlayerByCategoryQuerySchema(Schema):
    category = fields.Str(required=True)


class PlayerByTeamQuerySchema(Schema):
    team = fields.Str(required=True)
