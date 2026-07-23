from datetime import datetime, timezone
from sqlalchemy import UniqueConstraint, Index
from passlib.hash import bcrypt
from app.extensions import db
from app.models.enums import UserRole, DescriptorStatus

class TimestampMixin:
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

class Area(TimestampMixin, db.Model):
    __tablename__ = "areas"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False, index=True)

class Shift(TimestampMixin, db.Model):
    __tablename__ = "shifts"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True, nullable=False, index=True)

class Grade(TimestampMixin, db.Model):
    __tablename__ = "grades"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True, nullable=False)
    order = db.Column(db.Integer, nullable=False, index=True)

class ClassGroup(TimestampMixin, db.Model):
    __tablename__ = "class_groups"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, index=True)
    grade_id = db.Column(db.Integer, db.ForeignKey("grades.id", ondelete="RESTRICT"), nullable=False)
    shift_id = db.Column(db.Integer, db.ForeignKey("shifts.id", ondelete="RESTRICT"), nullable=False)
    grade = db.relationship("Grade")
    shift = db.relationship("Shift")
    __table_args__ = (UniqueConstraint("name", "shift_id", name="uq_class_shift"),)

class User(TimestampMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(160), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum(UserRole), nullable=False, default=UserRole.PCA)
    area_id = db.Column(db.Integer, db.ForeignKey("areas.id", ondelete="RESTRICT"), nullable=True)
    shift_id = db.Column(db.Integer, db.ForeignKey("shifts.id", ondelete="RESTRICT"), nullable=True)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    area = db.relationship("Area")
    shift = db.relationship("Shift")
    def set_password(self, password): self.password_hash = bcrypt.hash(password)
    def check_password(self, password): return bcrypt.verify(password, self.password_hash)

class Descriptor(TimestampMixin, db.Model):
    __tablename__ = "descriptors"
    id = db.Column(db.Integer, primary_key=True)
    area_id = db.Column(db.Integer, db.ForeignKey("areas.id", ondelete="RESTRICT"), nullable=False)
    grade_id = db.Column(db.Integer, db.ForeignKey("grades.id", ondelete="RESTRICT"), nullable=False)
    code = db.Column(db.String(40), nullable=False)
    description = db.Column(db.Text, nullable=False)
    deadline = db.Column(db.Date, nullable=False, index=True)
    notes = db.Column(db.Text)
    area = db.relationship("Area")
    grade = db.relationship("Grade")
    questions = db.relationship("Question", back_populates="descriptor", cascade="all, delete-orphan")
    __table_args__ = (UniqueConstraint("area_id", "grade_id", "code", name="uq_descriptor_area_grade_code"),)

class DescriptorApplication(TimestampMixin, db.Model):
    __tablename__ = "descriptor_applications"
    id = db.Column(db.Integer, primary_key=True)
    descriptor_id = db.Column(db.Integer, db.ForeignKey("descriptors.id", ondelete="CASCADE"), nullable=False)
    class_group_id = db.Column(db.Integer, db.ForeignKey("class_groups.id", ondelete="CASCADE"), nullable=False)
    status = db.Column(db.Enum(DescriptorStatus), nullable=False, default=DescriptorStatus.NOT_APPLIED)
    applied_at = db.Column(db.DateTime)
    descriptor = db.relationship("Descriptor")
    class_group = db.relationship("ClassGroup")
    __table_args__ = (UniqueConstraint("descriptor_id", "class_group_id", name="uq_descriptor_class_application"), Index("ix_application_status", "status"),)

class Question(TimestampMixin, db.Model):
    __tablename__ = "questions"
    id = db.Column(db.Integer, primary_key=True)
    descriptor_id = db.Column(db.Integer, db.ForeignKey("descriptors.id", ondelete="CASCADE"), nullable=False)
    text = db.Column(db.String(255), nullable=False)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    descriptor = db.relationship("Descriptor", back_populates="questions")

class Answer(TimestampMixin, db.Model):
    __tablename__ = "answers"
    id = db.Column(db.Integer, primary_key=True)
    application_id = db.Column(db.Integer, db.ForeignKey("descriptor_applications.id", ondelete="CASCADE"), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey("questions.id", ondelete="CASCADE"), nullable=False)
    answer = db.Column(db.Boolean, nullable=False)
    application = db.relationship("DescriptorApplication")
    question = db.relationship("Question")
    __table_args__ = (UniqueConstraint("application_id", "question_id", name="uq_answer_application_question"),)

class AuditLog(db.Model):
    __tablename__ = "audit_logs"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="SET NULL"))
    action = db.Column(db.String(120), nullable=False, index=True)
    entity = db.Column(db.String(120), nullable=False)
    entity_id = db.Column(db.Integer)
    metadata_json = db.Column(db.JSON)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False, index=True)
    user = db.relationship("User")
