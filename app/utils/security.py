from functools import wraps
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from flask_smorest import abort
from app.models.entities import User
from app.models.enums import UserRole

def current_user():
    user_id = get_jwt_identity()
    return User.query.get(user_id) if user_id else None

def roles_required(*roles):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            user = current_user()
            if not user or not user.is_active or user.role.value not in roles:
                abort(403, message="Acesso não autorizado para este recurso.")
            return fn(*args, **kwargs)
        return wrapper
    return decorator

def apply_pca_scope(query, user, model):
    if user.role == UserRole.ADMIN:
        return query
    return query.filter(model.area_id == user.area_id)
