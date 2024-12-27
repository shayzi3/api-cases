from typing import Sequence, Any, TypeVar, Generic
from abc import ABC, abstractmethod
from sqlalchemy import delete, select, insert, update
from src.db.models import Session


ModelSchema = TypeVar("ModelSchema")


class Repository(ABC):
     
     @abstractmethod
     async def create(values, **extras):
          raise NotImplementedError
     
     
     @abstractmethod
     async def read(values, **extras):
          raise NotImplementedError
     
     
     @abstractmethod
     async def update(where, **extras):
          raise NotImplementedError
     
     
     @abstractmethod
     async def delete(where, **extras):
          raise NotImplementedError
     
     



class ORMRepository(Generic[ModelSchema], Repository, Session):
     model: type | None = None
     
     async def create(
          self, 
          values: Sequence[str] = (),
          **extras
     ) -> ModelSchema | list[Any]:
          async with self.session.begin() as session:
               sttm = (
                    insert(self.model).
                    values(**extras)
               )
               await session.execute(sttm)
               await session.commit()
               
               return self.model.to_pydantic_model(self.model(**extras), *values)
     
     
     async def read(
          self, 
          values: Sequence[str] = (),
          **extras
     ) -> ModelSchema | list[Any] | None:
          """Read, get data from db

          Args:
              session (AsyncSession): AsyncSession
              values (Sequence[str] | None, optional): Arguments which must be returns. Default - ()
              **extras - where values

          Returns:
              ModelSchema | list[Any]
          """
          async with self.session() as session:
               sttm = select(self.model).filter_by(**extras)
               result = await session.execute(sttm)
               output = result.scalar()

               if not output:
                    return None
               return self.model.to_pydantic_model(output, *values)
     
     
     async def update(
          self, 
          where: dict[str, Any],
          **extras
     ) -> None:
          async with self.session.begin() as session:
               sttm = update(self.model).filter_by(**where).values(**extras)
               await session.execute(sttm)
     
     
     async def delete(
          self, 
          where: dict[str, Any],
          **extras
     ) -> None:
          return