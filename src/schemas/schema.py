from __future__ import annotations

from datetime import datetime
from pydantic import BaseModel


class ResponseModel(BaseModel):
     response: str
     status: int
     
     
class UserSchema(BaseModel):
     id: str
     username: str
     email: str
     cash: int
     created_at: datetime
     is_verifed: bool
     inventory: list[ItemSchema | None]
     
     
     
     
class CaseSchema(BaseModel):
     id: int
     name: str
     price: int
     image: str
     items: list[ItemSchema | None]
     
     
class ItemSchema(BaseModel):
     id: int
     name: str
     price: int
     cases: list[CaseSchema | None]
     users: list[UserSchema | None]
     
     
class TokenSchema(BaseModel):
     token: str
     type: str
     
     def __str__(self) -> str:
          return f'{self.type.title()} {self.token}'
     
     
class TokenData(BaseModel):
     id: str
     username: str
     email: str
     is_verifed: bool
     iat: datetime
     exp: datetime