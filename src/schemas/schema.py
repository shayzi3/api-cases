from __future__ import annotations

from pydantic import BaseModel


class ResponseModel(BaseModel):
     response: str
     status: int
     
     
class UserSchema(BaseModel):
     id: str
     name: str
     email: str
     cash: int
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
