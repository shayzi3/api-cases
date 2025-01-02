from pydantic import BaseModel
from src.schemas.schema import ItemSchemaForUserCase




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