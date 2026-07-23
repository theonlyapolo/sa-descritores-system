from app.models.entities import Area, Shift, Grade, ClassGroup, User, Descriptor, DescriptorApplication, Question, Answer, AuditLog
from app.repositories.base import BaseRepository

class AreaRepository(BaseRepository): model = Area
class ShiftRepository(BaseRepository): model = Shift
class GradeRepository(BaseRepository): model = Grade
class ClassGroupRepository(BaseRepository): model = ClassGroup
class UserRepository(BaseRepository): model = User
class DescriptorRepository(BaseRepository): model = Descriptor
class ApplicationRepository(BaseRepository): model = DescriptorApplication
class QuestionRepository(BaseRepository): model = Question
class AnswerRepository(BaseRepository): model = Answer
class AuditLogRepository(BaseRepository): model = AuditLog
