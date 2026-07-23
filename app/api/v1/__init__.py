from .auth import blp as auth_blp
from .resources import blp as resources_blp
from .dashboard import blp as dashboard_blp

def register_blueprints(api):
    api.register_blueprint(auth_blp)
    api.register_blueprint(resources_blp)
    api.register_blueprint(dashboard_blp)
