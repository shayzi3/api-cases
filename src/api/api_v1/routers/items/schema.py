from typing import Any
from pydantic import BaseModel, ConfigDict, Field

from src.core import generate_id
from .enum import Quality


class ItemBody(BaseModel):
     model_config = ConfigDict(use_enum_values=True)
     
     name: str
     price: int
     quality: Quality
     
     
     
class ItemBodyNullable(BaseModel):
     # For patch endpoint /api/v1/items
     model_config = ConfigDict(use_enum_values=True)
     
     name: str = Field(default="Null")
     price: int = Field(default="Null")
     quality: Quality = Field(
          default=Quality.NULL, validate_default=True
     )
     
     @property
     def not_nullable(self) -> dict[str, Any]:
          arguments = {}
          for key, value in self.model_dump().items():
               if value != "Null":
                    arguments[key] = value
          return arguments
          
     
     
class ItemBodyID(ItemBody):
     id: str = generate_id()