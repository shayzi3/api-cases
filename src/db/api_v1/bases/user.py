from sqlalchemy import select

from src.db.api_v1.repository import ORMRepository
from src.db.api_v1.models import User
from src.schemas.api_v1 import UserSchema, UserWithPassword
from src.core.api_v1.security import verify_password


class UserRepository(ORMRepository[UserSchema]):
     model = User
     
     
     async def read_with_password(self, **extras) -> UserWithPassword | bool:
          async with self.session() as session:
               sttm = select(self.model).filter_by(**extras)
               result = await session.execute(sttm)
               output = result.scalar()
               
               if not output:
                    return False
               return UserWithPassword(**output.__dict__)
          
          
     async def check_user_password(self, password: str, **extras) -> bool:
          async with self.session() as session:
               sttm = select(self.model).filter_by(**extras)
               result = await session.execute(sttm)
               output = result.scalar()
                
               if not output:
                    return False
               return verify_password(password, output.password)
               