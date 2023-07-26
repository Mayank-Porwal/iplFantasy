from marshmallow import Schema, fields


class PlayerResponseSchema(Schema):
    id = fields.Int(required=True)
    name = fields.Str(required=True)
    team = fields.Str(required=True, attribute='ipl_team')
    category = fields.Str(required=True)
    cap = fields.Int(required=True)
    img = fields.Str(required=True, attribute='image_file')



class PlayerByCategoryQuerySchema(Schema):
    category = fields.Str(required=True)


class PlayerByTeamQuerySchema(Schema):
    team = fields.Str(required=True)