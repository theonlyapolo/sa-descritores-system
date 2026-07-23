from flask.views import MethodView
from flask_smorest import Blueprint
from marshmallow import Schema, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from app.models.entities import User
from app.services.auth import AuthService
from app.schemas.entities import UserSchema

blp = Blueprint("auth", __name__, url_prefix="/api/v1/auth", description="Autenticação JWT")
class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True)
class TokenSchema(Schema):
    access_token = fields.Str(); refresh_token = fields.Str(); user = fields.Nested(UserSchema)

@blp.route("/login")
class Login(MethodView):
    @blp.arguments(LoginSchema)
    @blp.response(200, TokenSchema)
    def post(self, data): return AuthService().login(**data)

@blp.route("/refresh")
class Refresh(MethodView):
    @jwt_required(refresh=True)
    def post(self): return {"access_token": create_access_token(identity=get_jwt_identity())}

@blp.route("/me")
class Me(MethodView):
    @jwt_required()
    @blp.response(200, UserSchema)
    def get(self): return User.query.get_or_404(get_jwt_identity())

@blp.route("/logout")
class Logout(MethodView):
    @jwt_required()
    def post(self): return {"message": "Logout efetuado no cliente; descarte o token JWT."}
