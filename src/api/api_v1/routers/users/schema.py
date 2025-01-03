from __future__ import annotations

from datetime import datetime
from typing import Any
from pydantic import BaseModel, Field, field_validator, EmailStr

from src.core.api_v1 import generate_id
from src.core.api_v1.security import hashed_password
     
     
     
class RegisterUserSchema(BaseModel):
     username: str
     password: str
     email: EmailStr
     
     
     @field_validator("email")
     @classmethod
     def validate_email(cls, email_str: str):
          email_prefix = email_str.split("@")[-1]
          
          if email_prefix != "mail.ru":
               raise ValueError("Email must be mail.ru")
          return email_str
     
     
     
class RegisterUser(RegisterUserSchema):
     id: str = generate_id()
     cash: int = 0
     low_chanse: float = 85.5
     high_chanse: float = 14.5
     is_verifed: bool = False
     is_admin: bool = False
     created_at: datetime = datetime.now()
     avatar: str | None = None
     
     @field_validator("password")
     @classmethod
     def password_hash(cls, psw: str):
          return hashed_password(psw)
     
     
class LoginUserSchema(BaseModel):
     username: str
     password: str
     
     

class UserBodyNullable(BaseModel):
     username: str = Field(default="Null")
     email: str = Field(default="Null")
     
     
     @field_validator("email")
     @classmethod
     def validate_email(cls, email_str: str):
          if email_str != "Null":
               email_prefix = email_str.split("@")[-1]
               
               if email_prefix != "mail.ru":
                    raise ValueError("Email must be mail.ru")
          return email_str
          
          
     @property
     def not_nullable(self) -> dict[str, Any]:
          arguments = {}
          for key, value in self.model_dump().items():
               if value != "Null":
                    arguments[key] = value
          return arguments
     
     