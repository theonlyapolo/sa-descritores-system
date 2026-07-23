from datetime import date
from app import create_app
from app.config import TestConfig
from app.extensions import db
from app.models.entities import Area, Shift, Grade, ClassGroup, User, Descriptor, DescriptorApplication
from app.models.enums import UserRole


def seed():
    area=Area(name="Humanas"); shift=Shift(name="Matutino"); grade=Grade(name="6º Ano", order=6)
    db.session.add_all([area, shift, grade]); db.session.flush()
    klass=ClassGroup(name="6 M01", grade_id=grade.id, shift_id=shift.id)
    user=User(name="PCA", email="pca@example.com", role=UserRole.PCA, area_id=area.id, shift_id=shift.id); user.set_password("password123")
    desc=Descriptor(area_id=area.id, grade_id=grade.id, code="D1", description="Teste", deadline=date.today())
    db.session.add_all([klass, user, desc]); db.session.flush()
    db.session.add(DescriptorApplication(descriptor_id=desc.id, class_group_id=klass.id))
    db.session.commit()


def test_login_and_pca_dashboard():
    app=create_app(TestConfig)
    with app.app_context():
        db.create_all(); seed()
    client=app.test_client()
    res=client.post("/api/v1/auth/login", json={"email":"pca@example.com","password":"password123"})
    assert res.status_code == 200
    token=res.get_json()["access_token"]
    dash=client.get("/api/v1/dashboard/pca", headers={"Authorization":f"Bearer {token}"})
    assert dash.status_code == 200
    assert dash.get_json()["pending"] == 1
