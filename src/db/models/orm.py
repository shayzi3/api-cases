
from typing import Sequence, Any, TypeVar, Generic
from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete, select, insert, update


ModelSchema = TypeVar("ModelSchema")


class OrmRepository(ABC):
     
     @abstractmethod
     def create(session, values, **extras):
          raise NotImplementedError
     
     
     @abstractmethod
     def read(session, values, **extras):
          raise NotImplementedError
     
     
     @abstractmethod
     def update(session, values, **extras):
          raise NotImplementedError
     
     
     @abstractmethod
     def delete(session, values, **extras):
          raise NotImplementedError
     
     



class OrmBasedClassMixin(Generic[ModelSchema], OrmRepository):
     model: type | None = None
     
     @classmethod
     async def create(
          cls, 
          session: AsyncSession, 
          values: Sequence[str | None] = (),
          **extras
     ) -> ModelSchema | list[Any]:
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
     ) -> ModelSchema | list[Any]:
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