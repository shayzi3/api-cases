from pydantic import BaseModel, field_validator

from src.core import generate_id
from src.schemas.enums import Quality
from src.schemas.users import UserSchema
from src.schemas.cases import CaseSchema
from src.schemas.schema import ItemSchemaForUserCase


class ItemBody(BaseModel):
     name: str
     price: int
     quality: Quality
     
     
     @field_validator("quality")
     @classmethod
     def validate_quality(cls, qua: Quality):
          return qua.value
     
     
class ItemBodyID(ItemBody):
     id: str = generate_id()
     
     
     
class ItemSchema(ItemSchemaForUserCase):
     cases: list[CaseSchema]
     users: list[UserSchema]