import json

from datetime import datetime
from typing import Any
from pydantic import BaseModel, field_validator, EmailStr
from src.schemas.schema import ItemSchemaForUserCase

from src.core import generate_id
from src.core.security import hashed_password




class UserSchema(BaseModel):
     id: str
     username: str
     email: str
     cash: int
     created_at: datetime
     is_verifed: bool
     is_admin: bool
     inventory: list[ItemSchemaForUserCase]
     avatar: str | None = None
     
     
     def convert_to_redis(self) -> str:
          self.created_at = self.created_at.timestamp() # json cant convert datetime type
          return json.dumps(self.__dict__)
     
     @staticmethod
     def convert_from_redis(data: str) -> "UserSchema":
          data: dict = json.loads(data)
          data["created_at"] = datetime.utcfromtimestamp(data["created_at"])
          
          return UserSchema(**data)
     
     
class UserWithPassword(UserSchema):
     password: str
     
     
     
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
     
     def __str__(self) -> dict[str, Any]:
          return self.__dict__
     
     
     
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
     
     
     def __str__(self) -> dict[str, Any]:
          return self.__dict__
     
     
     
     
class LoginUserSchema(BaseModel):
     username: str
     password: str