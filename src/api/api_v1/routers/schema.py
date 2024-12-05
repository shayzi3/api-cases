
from pydantic import BaseModel, EmailStr
from src.core import generate_id


class RegisterUserSchema(BaseModel):
     name: str
     password: str
     email: EmailStr
    
     
class RegisterUser(RegisterUserSchema):
     id: str = generate_id()
     cash: int = 0
     low_chanse: float = 85.5
     high_chanse: float = 14.5
     inventory: list = []
     is_verifed: bool = False
     
     
class LoginUserSchema(BaseModel):
     email: str
     password: str