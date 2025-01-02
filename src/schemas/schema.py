from typing import Any
from datetime import datetime
from pydantic import BaseModel



class ResponseModel(BaseModel):
     response: str
     status: int
     
     
class TokenSchema(BaseModel):
     token: str
     type: str
     
     def __str__(self) -> str:
          return self.token
     
     
class ItemSchemaForUserCase(BaseModel):
     id: str
     name: str
     price: int
     quality: str
     
     
class TokenData(BaseModel):
     id: str
     username: str
     email: str
     is_verifed: bool
     is_admin: bool
     iat: datetime
     exp: datetime
     
     
     def verify(self) -> dict[str, Any]:
          self.is_verifed = True
          return self.__dict__
     
     @property
     def redis_values(self) -> list[str]:
          """Return: [user:id, user:username]"""
          return [f"user:{self.id}", f"user:{self.username}"]