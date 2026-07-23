from marshmallow import Schema, fields, validate

class AreaSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=2, max=120))

class ShiftSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)

class GradeSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    order = fields.Int(required=True)

class ClassGroupSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    grade_id = fields.Int(required=True, load_only=True)
    shift_id = fields.Int(required=True, load_only=True)
    grade = fields.Nested(GradeSchema, dump_only=True)
    shift = fields.Nested(ShiftSchema, dump_only=True)

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(load_only=True, validate=validate.Length(min=8))
    role = fields.Str(required=True, validate=validate.OneOf(["Administrador", "PCA"]))
    area_id = fields.Int(allow_none=True)
    shift_id = fields.Int(allow_none=True)
    is_active = fields.Bool(dump_only=True)
    area = fields.Nested(AreaSchema, dump_only=True)
    shift = fields.Nested(ShiftSchema, dump_only=True)

class DescriptorSchema(Schema):
    id = fields.Int(dump_only=True)
    area_id = fields.Int(required=True)
    grade_id = fields.Int(required=True)
    code = fields.Str(required=True)
    description = fields.Str(required=True)
    deadline = fields.Date(required=True)
    notes = fields.Str(allow_none=True)
    area = fields.Nested(AreaSchema, dump_only=True)
    grade = fields.Nested(GradeSchema, dump_only=True)

class ApplicationSchema(Schema):
    id = fields.Int(dump_only=True)
    descriptor_id = fields.Int(required=True)
    class_group_id = fields.Int(required=True)
    status = fields.Str(validate=validate.OneOf(["Aplicado", "Não Aplicado"]))
    descriptor = fields.Nested(DescriptorSchema, dump_only=True)
    class_group = fields.Nested(ClassGroupSchema, dump_only=True)
    applied_at = fields.DateTime(dump_only=True)

class QuestionSchema(Schema):
    id = fields.Int(dump_only=True)
    descriptor_id = fields.Int(required=True)
    text = fields.Str(required=True)
    is_active = fields.Bool()

class AnswerSchema(Schema):
    id = fields.Int(dump_only=True)
    application_id = fields.Int(required=True)
    question_id = fields.Int(required=True)
    answer = fields.Bool(required=True)


class AuditLogSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int(allow_none=True)
    action = fields.Str(required=True)
    entity = fields.Str(required=True)
    entity_id = fields.Int(allow_none=True)
    metadata_json = fields.Dict(allow_none=True)
    created_at = fields.DateTime(dump_only=True)
