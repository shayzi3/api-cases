
from datetime import datetime
from pydantic import BaseModel, EmailStr
from src.core import generate_id


class RegisterUserSchema(BaseModel):
     username: str
     password: str
     email: EmailStr
    
     
class RegisterUser(RegisterUserSchema):
     id: str = generate_id()
     cash: int = 0
     low_chanse: float = 85.5
     high_chanse: float = 14.5
     is_verifed: bool = False
     created_at: datetime = datetime.now()
     
     
class LoginUserSchema(BaseModel):
     email: str
     password: str