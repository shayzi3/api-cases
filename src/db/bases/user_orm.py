from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, insert

from src.schemas import UserSchema
from src.db.models import User
from src.core import Crud




class ORMBaseUser(Crud):
     
     @staticmethod
     async def create(session: AsyncSession, **extras) -> UserSchema:
          async with session.begin():
               sttm = (
                    insert(User).
                    values(**extras)
               )
               await session.execute(sttm)
     
     @staticmethod
     async def read(session: AsyncSession, **extras) -> UserSchema | None:
          async with session():
               sttm = select(User).where(**extras)
               result = await session.execute(sttm)

               if not result.scalar():
                    return None
          return UserSchema(**result.scalar().__dict__)
     
     @classmethod
     async def update(cls, session: AsyncSession, **extras):
          return
     
     @classmethod
     async def delete(cls, session: AsyncSession, **extras):
          return