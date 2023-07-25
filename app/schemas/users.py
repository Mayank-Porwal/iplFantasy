from marshmallow import Schema, fields


class UserRegisterSchema(Schema):
    id = fields.Int(dump_only=True)
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    password = fields.Str(required=True)
    email = fields.Str(required=True)
    phone_number = fields.Str(required=True)


class UserLoginSchema(Schema):
    id = fields.Int(dump_only=True)
    email = fields.Str(required=True)
    password = fields.Str(required=True)
