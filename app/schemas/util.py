from marshmallow import Schema, fields


class PostResponseSuccessSchema(Schema):
    message = fields.Str(dump_only=True)
