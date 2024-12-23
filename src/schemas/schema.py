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