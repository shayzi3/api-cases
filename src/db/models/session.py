
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from src.core import settings




class Session:
     engine = create_async_engine(settings.postgres, echo=True)
     session = async_sessionmaker(engine)