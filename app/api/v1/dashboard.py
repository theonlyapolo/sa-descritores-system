from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import jwt_required
from app.services.dashboard import DashboardService
from app.utils.security import current_user, roles_required

blp = Blueprint("dashboard", __name__, url_prefix="/api/v1", description="Dashboards e alertas")

@blp.route("/dashboard/pca")
class PcaDashboard(MethodView):
    @jwt_required()
    def get(self): return DashboardService().pca_dashboard(current_user())

@blp.route("/dashboard/admin")
class AdminDashboard(MethodView):
    @roles_required("Administrador")
    def get(self): return DashboardService().admin_dashboard()

@blp.route("/alerts")
class Alerts(MethodView):
    @jwt_required()
    def get(self): return {"alerts": DashboardService().alerts(current_user())}
