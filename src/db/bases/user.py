from src.db.repository import ORMRepository
from src.db.models import User
from src.schemas import UserSchema


class UserRepository(ORMRepository[UserSchema]):
     model = User