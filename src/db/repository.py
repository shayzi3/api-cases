from typing import Sequence, Any, TypeVar, Generic
from abc import ABC, abstractmethod
from sqlalchemy import delete, select, insert, update

from src.db.models import Session
from src.services.redis import RedisPool



PydanticSchema = TypeVar("PydanticSchema")


class AbstractRepository(ABC):
     
     @abstractmethod
     async def create(values, **extras):
          raise NotImplementedError
     
     
     @abstractmethod
     async def read(values, **extras):
          raise NotImplementedError
     
     
     @abstractmethod
     async def update(redis_value, where, **extras):
          raise NotImplementedError
     
     
     @abstractmethod
     async def delete(redis_value, where, **extras):
          raise NotImplementedError
     
     



class ORMRepository(Generic[PydanticSchema], AbstractRepository, Session):
     model: type | None = None
     
     async def create(
          self, 
          values: Sequence[str] = (),
          **extras
     ) -> PydanticSchema | list[Any]:
          """Create

          Args:
              values (Sequence[str], optional): Values which will be return. Defaults to ().
              extras - valaues for save in db

          Returns:
               PydanticSchema | list[Any]:
                    list[Any] - keep values which come from argument:`values`
          """
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
     ) -> PydanticSchema | list[Any] | None:
          """Read, get data from db

          Args:
              values (Sequence[str] | None, optional): Arguments which must be returns. Default - ()
              **extras - where values

          Returns:
               PydanticSchema | list[Any]
                    list[Any] - keep values which come from argument:`values`
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
          redis_value: list[str] = [],
          **extras
     ) -> None:
          """Update

          Args:
              where (dict[str, Any]): where values
              redis_value (list[str], optional): Delete user from Redis. Defaults to [].
              extras - values for save in db
          """
          async with self.session.begin() as session:
               sttm = update(self.model).filter_by(**where).values(**extras)
               await session.execute(sttm)
               
          if redis_value:
               await RedisPool().delete(*redis_value)
     
     
     async def delete(
          self, 
          where: dict[str, Any],
          redis_value: list[str] = [],
     ) -> None:
          """Delete

          Args:
              where (dict[str, Any]): where values
              redis_value (list[str], optional): Delete user from Redis. Defaults to [].
          """
          async with self.session.begin() as session:
               sttm = delete(self.model).filter_by(**where)
               await session.execute(sttm)
          
          if redis_value:
               await RedisPool().delete(*redis_value)