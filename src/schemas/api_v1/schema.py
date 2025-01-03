from __future__ import annotations

import json

from typing import Any
from datetime import datetime
from pydantic import BaseModel




class ItemSchemaForUserCase(BaseModel):
     id: str
     name: str
     price: int
     quality: str
     


class UserSchema(BaseModel):
     id: str
     username: str
     email: str
     cash: int
     created_at: datetime
     is_verifed: bool
     is_admin: bool
     is_banned: bool
     inventory: list[ItemSchemaForUserCase]
     avatar: str | None = None
     
     
     def convert_to_redis(self) -> str:
          self.created_at = self.created_at.timestamp() # json cant convert datetime type
          return json.dumps(self.__dict__)
     
     @staticmethod
     def convert_from_redis(data: str) -> UserSchema:
          data: dict = json.loads(data)
          data["created_at"] = datetime.utcfromtimestamp(data["created_at"])
          
          return UserSchema(**data)
     
     
class UserWithPassword(UserSchema):
     password: str
     
     
class CaseSchema(BaseModel):
     id: str
     name: str
     price: int
     image: str
     items: list[ItemSchemaForUserCase]
     
     @property
     def redis_values(self) -> list[str]:
          """Return: [case:id, case:name]"""
          return [f"case:{self.id}", f"case:{self.name}"]
     
     
     
class ItemSchema(ItemSchemaForUserCase):
     cases: list[CaseSchema]
     users: list[UserSchema]
     
     
     def convert_to_redis(self) -> str:
          return json.dumps(self.__dict__)
     
     
     @staticmethod
     def convert_from_redis(data: str) -> "ItemSchema":
          new_data: dict = json.loads(data)
          return ItemSchema(**new_data)
     
     
     @property
     def redis_values(self) -> list[str]:
          """Return: [item:id, item:username]"""
          return [f"item:{self.id}", f"item:{self.name}"]
     
     

class ResponseModel(BaseModel):
     response: str
     status: int
     
     
     
class TokenSchema(BaseModel):
     token: str
     type: str
     
     def __str__(self) -> str:
          return self.token
     
     
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