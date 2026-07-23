from flask_smorest import abort
from flask_jwt_extended import create_access_token, create_refresh_token
from app.models.entities import User

class AuthService:
    def login(self, email, password):
        user = User.query.filter_by(email=email).first()
        if not user or not user.is_active or not user.check_password(password):
            abort(401, message="Credenciais inválidas.")
        identity = str(user.id)
        return {"access_token": create_access_token(identity=identity), "refresh_token": create_refresh_token(identity=identity), "user": user}
