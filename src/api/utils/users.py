from typing_extensions import Self, Any
from fastapi import HTTPException, status, UploadFile
from loguru import logger

from src.services.storage3 import Storage3
from src.db.bases import UserRepository
from src.core import settings




class UsersGetBy:
     __slots__ = ("__data",)
     
     def __init__(self):
          self.__data = {}
          
     
     def get_by(
          self,
          request_user_id: str,
          id: str | None = None,
          username: str | None = None,
     ) -> Self:
          self.__data = {"username": username} if username else {"id": id}
          
          if (id is None) and (username is None):
               self.__data = {"id": request_user_id}
          return self
     
     
     @property 
     def data_value(self) -> str | None:
          """{id: 123} -> user:123"""
          
          if self.__data:
               return f"user:{list(self.__data.values())[0]}"
          
          
     @property
     def data(self) -> dict[str, Any]:
          return self.__data



async def valide_file(file: UploadFile) -> UploadFile | None:
     if not file:
          return None
     
     if file.filename.split(".")[-1] not in ["jpg", "png"]:
          raise HTTPException(
               detail="File must be jpg or png!",
               status_code=status.HTTP_403_FORBIDDEN
          )
     return file


async def background_upload_avatar(
     file: bytes,
     filename: str,
     user_id: str,
     redis_values: list[str]
) -> None:
     url_avatar = settings.s3_url + filename
     
     await Storage3.upload_file(
          file=file,
          name=filename
     )
     await UserRepository().update(
          where={"id": user_id},
          redis_value=redis_values,
          avatar=url_avatar
     )
     
     logger.info(f"SUCCESS UPLOAD AVATAR FOR {user_id}")
     
     
async def background_delete_avatar(
     filename: str,
     user_id: str,
     redis_values: list[str]
) -> None:
     await UserRepository().update(
          where={"id": user_id},
          redis_value=redis_values,
          avatar=None
     )
     await Storage3.delete_file(name=filename)
     
     logger.info(f"SUCCESS DELETE AVATAR FOR {user_id}")
     