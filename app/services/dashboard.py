from datetime import date, timedelta
from sqlalchemy import func
from app.models.entities import DescriptorApplication, Descriptor, ClassGroup
from app.models.enums import DescriptorStatus, UserRole

class DashboardService:
    def scoped_applications(self, user):
        q = DescriptorApplication.query.join(Descriptor).join(ClassGroup)
        if user.role == UserRole.PCA:
            q = q.filter(Descriptor.area_id == user.area_id, ClassGroup.shift_id == user.shift_id)
        return q
    def pca_dashboard(self, user):
        apps = self.scoped_applications(user).all()
        total = len(apps); done = sum(a.status == DescriptorStatus.APPLIED for a in apps)
        classes = ClassGroup.query.filter_by(shift_id=user.shift_id).all()
        return {"completed": done, "pending": total-done, "percent_completed": round((done/total)*100, 2) if total else 0, "classes": [{"id": c.id, "name": c.name} for c in classes], "summary": {"area_id": user.area_id, "shift_id": user.shift_id, "total": total}}
    def admin_dashboard(self):
        apps = DescriptorApplication.query.join(Descriptor).join(ClassGroup).all()
        total = len(apps); done = sum(a.status == DescriptorStatus.APPLIED for a in apps)
        late = sum(a.status != DescriptorStatus.APPLIED and a.descriptor.deadline < date.today() for a in apps)
        by_area = dict(DescriptorApplication.query.join(Descriptor).with_entities(Descriptor.area_id, func.count(DescriptorApplication.id)).group_by(Descriptor.area_id).all())
        by_shift = dict(DescriptorApplication.query.join(ClassGroup).with_entities(ClassGroup.shift_id, func.count(DescriptorApplication.id)).group_by(ClassGroup.shift_id).all())
        return {"totals": {"completed": done, "pending": total-done, "late": late}, "percent_completed": round((done/total)*100,2) if total else 0, "charts": {"by_area": by_area, "by_shift": by_shift, "history": []}}
    def alerts(self, user):
        today = date.today(); soon = today + timedelta(days=7); alerts=[]
        apps = self.scoped_applications(user).filter(DescriptorApplication.status != DescriptorStatus.APPLIED).all()
        late = [a for a in apps if a.descriptor.deadline < today]
        due = [a for a in apps if today <= a.descriptor.deadline <= soon]
        if late: alerts.append({"type":"overdue","color":"danger","message":f"Existem {len(late)} descritores atrasados."})
        if due: alerts.append({"type":"due_soon","color":"warning","message":f"Existem {len(due)} descritores próximos do vencimento."})
        if not alerts: alerts.append({"type":"ok","color":"success","message":"Todos os descritores estão dentro do prazo."})
        return alerts
