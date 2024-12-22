from pydantic import BaseModel
from src.schemas.schema import ItemSchemaForUserCase




class CaseSchema(BaseModel):
     id: str
     name: str
     price: int
     image: str
     items: list[ItemSchemaForUserCase]