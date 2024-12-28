from typing import Any, Optional
from pydantic import BaseModel, ConfigDict, Field

from src.core import generate_id
from src.schemas.enums import Quality
from src.schemas.users import UserSchema
from src.schemas.cases import CaseSchema
from src.schemas.schema import ItemSchemaForUserCase


class ItemBody(BaseModel):
     model_config = ConfigDict(use_enum_values=True)
     
     name: str
     price: int
     quality: Quality
     
     
     
class ItemBodyNullable(BaseModel):
     # For patch endpoint /api/v1/items
     model_config = ConfigDict(use_enum_values=True)
     
     name: Optional[str] = Field(default="Null")
     price: Optional[int] = Field(default="Null")
     quality: Optional[Quality] = Field(
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
     
     
class ItemSchema(ItemSchemaForUserCase):
     cases: list[CaseSchema]
     users: list[UserSchema]