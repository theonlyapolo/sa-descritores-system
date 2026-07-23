from marshmallow import Schema, fields

class MessageSchema(Schema):
    message = fields.String(required=True)

class PaginationSchema(Schema):
    page = fields.Integer(load_default=1)
    per_page = fields.Integer(load_default=20)
    sort = fields.String(load_default="id")
