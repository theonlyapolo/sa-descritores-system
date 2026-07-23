from datetime import datetime, timezone
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required
from app.extensions import db
from app.models.entities import Area, Shift, Grade, ClassGroup, User, Descriptor, DescriptorApplication, Question, Answer, AuditLog
from app.models.enums import UserRole, DescriptorStatus
from app.schemas.entities import AreaSchema, ShiftSchema, GradeSchema, ClassGroupSchema, UserSchema, DescriptorSchema, ApplicationSchema, QuestionSchema, AnswerSchema, AuditLogSchema
from app.utils.security import current_user, roles_required

blp = Blueprint("resources", __name__, url_prefix="/api/v1", description="Recursos administrativos e operacionais")

def crud(model, schema, route, admin_only=True):
    @blp.route(route, endpoint=f"{model.__name__.lower()}_collection")
    class Collection(MethodView):
        @jwt_required()
        @blp.response(200, schema(many=True))
        def get(self): return model.query.all()
        @roles_required("Administrador") if admin_only else jwt_required()
        @blp.arguments(schema)
        @blp.response(201, schema)
        def post(self, data):
            obj = model(**data)
            if isinstance(obj, User) and data.get("password"): obj.set_password(data["password"])
            db.session.add(obj); db.session.commit(); return obj
    @blp.route(f"{route}/<int:item_id>", endpoint=f"{model.__name__.lower()}_item")
    class Item(MethodView):
        @jwt_required()
        @blp.response(200, schema)
        def get(self, item_id): return model.query.get_or_404(item_id)
        @roles_required("Administrador") if admin_only else jwt_required()
        @blp.arguments(schema(partial=True))
        @blp.response(200, schema)
        def patch(self, data, item_id):
            obj = model.query.get_or_404(item_id)
            password = data.pop("password", None)
            for k, v in data.items(): setattr(obj, k, v)
            if password and isinstance(obj, User): obj.set_password(password)
            db.session.commit(); return obj
        @roles_required("Administrador")
        def delete(self, item_id):
            db.session.delete(model.query.get_or_404(item_id)); db.session.commit(); return {"message":"Removido com sucesso."}

crud(Area, AreaSchema, "/areas"); crud(Shift, ShiftSchema, "/shifts"); crud(Grade, GradeSchema, "/grades")
crud(ClassGroup, ClassGroupSchema, "/classes"); crud(User, UserSchema, "/users"); crud(Descriptor, DescriptorSchema, "/descriptors")
crud(Question, QuestionSchema, "/questions"); crud(Answer, AnswerSchema, "/answers", admin_only=False); crud(AuditLog, AuditLogSchema, "/logs")

@blp.route("/applications")
class Applications(MethodView):
    @jwt_required()
    @blp.response(200, ApplicationSchema(many=True))
    def get(self):
        user = current_user(); q = DescriptorApplication.query.join(Descriptor).join(ClassGroup)
        if user.role == UserRole.PCA:
            q = q.filter(Descriptor.area_id == user.area_id, ClassGroup.shift_id == user.shift_id)
        return q.all()
    @roles_required("Administrador")
    @blp.arguments(ApplicationSchema)
    @blp.response(201, ApplicationSchema)
    def post(self, data):
        obj = DescriptorApplication(**data); db.session.add(obj); db.session.commit(); return obj

@blp.route("/applications/<int:item_id>")
class ApplicationItem(MethodView):
    @jwt_required()
    @blp.arguments(ApplicationSchema(partial=True))
    @blp.response(200, ApplicationSchema)
    def patch(self, data, item_id):
        user = current_user(); obj = DescriptorApplication.query.get_or_404(item_id)
        if user.role == UserRole.PCA and (obj.descriptor.area_id != user.area_id or obj.class_group.shift_id != user.shift_id):
            abort(403, message="PCA só pode alterar descritores da própria área e turno.")
        if data.get("status") == DescriptorStatus.APPLIED.value: obj.applied_at = datetime.now(timezone.utc)
        for k,v in data.items(): setattr(obj, k, v)
        db.session.commit(); return obj
