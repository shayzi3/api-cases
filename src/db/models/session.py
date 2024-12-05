
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from src.core import settings


engine = create_async_engine(settings().postgres, echo=True)


async def get_db_session() -> AsyncGenerator[None, AsyncSession]:
     session = async_sessionmaker(engine)
     
     async with session() as connection:
          yield connection
     await connection.close()