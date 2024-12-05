from __future__ import annotations

from datetime import datetime
from typing import Generic, TypeVar
from pydantic import BaseModel


class ResponseModel(BaseModel):
     response: str
     status: int
     
     
class UserSchema(BaseModel):
     id: str
     name: str
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
     
     
     
S = TypeVar("S")
     
class AllSchemas(Generic[S]):
     ...
