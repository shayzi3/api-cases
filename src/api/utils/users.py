from typing_extensions import Self, Any
from fastapi import UploadFile, HTTPException, status




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



async def valide_file(file: UploadFile) -> UploadFile:
     if file.filename.split(".")[-1] not in ["jpg", "png"]:
          raise HTTPException(
               detail="File must be jpg or png!",
               status_code=status.HTTP_403_FORBIDDEN
          )
     return file