from sqlalchemy import select

from src.db.repository import ORMRepository
from src.db.models import User
from src.schemas import UserSchema, UserWithPassword


class UserRepository(ORMRepository[UserSchema]):
     model = User
     
     
     async def read_with_password(self, **extras) -> UserWithPassword:
          async with self.session() as session:
               sttm = select(self.model).filter_by(**extras)
               result = await session.execute(sttm)
               output = result.scalar()

               if not output:
                    return None
               return UserWithPassword(**output.__dict__)