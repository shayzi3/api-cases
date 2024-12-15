
from datetime import datetime
from pydantic import BaseModel, EmailStr, field_validator
from src.core import generate_id


class RegisterUserSchema(BaseModel):
     username: str
     password: str
     email: EmailStr
     
     
     @field_validator('email')
     @classmethod
     def validate_email(cls, email_str: str):
          email_prefix = email_str.split('@')[-1]
          
          if email_prefix != 'mail.ru':
               raise ValueError('Email must be mail.ru')
          return email_str
     
     
     
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