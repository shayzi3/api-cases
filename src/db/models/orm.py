
from typing import Sequence, Union, Any
from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete, select, insert, update
from src.schemas import UserSchema, ItemSchema, CaseSchema


Schemas = Union[UserSchema, ItemSchema, CaseSchema, list[Any]]


class OrmRepository(ABC):
     
     @abstractmethod
     def create(session, **extras):
          raise NotImplementedError
     
     
     @abstractmethod
     def read(session, **extras):
          raise NotImplementedError
     
     
     @abstractmethod
     def update(session, **extras):
          raise NotImplementedError
     
     
     @abstractmethod
     def delete(session, **extras):
          raise NotImplementedError
     
     


class OrmBasedClassMixin(OrmRepository):
     model: type = None
     
     
     @classmethod
     async def create(
          cls, 
          session: AsyncSession, 
          values: Sequence[str | None] = (),
          **extras
     ) -> Schemas:
          sttm = (
               insert(cls.model).
               values(**extras)
          )
          await session.execute(sttm)
          await session.commit()
          
          return cls.model.to_pydantic_model(cls.model(**extras), *values)
     
     
     @classmethod
     async def read(
          cls, 
          session: AsyncSession, 
          values: Sequence[str] | None = (),
          **extras
     ) -> Schemas:
          sttm = select(cls.model).filter_by(**extras)
          result = await session.execute(sttm)
          output = result.scalar()

          if not output:
               return None
          return cls.model.to_pydantic_model(output, *values)
     
     
     @classmethod
     async def update(cls, session: AsyncSession, **extras):
          return
     
     
     @classmethod
     async def delete(cls, session: AsyncSession, **extras):
          return