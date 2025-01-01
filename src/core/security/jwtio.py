from typing import TypeVar
from datetime import timedelta, datetime
from fastapi import HTTPException, status
from jose import jwt, JWTError

from src.schemas import TokenSchema, TokenData
from src.core import settings


PydanticSchema = TypeVar("PydanticSchema")


async def create_token(schema: PydanticSchema | None = None, **kwargs) -> TokenSchema:
     if schema:
          kwargs["id"] = schema.id
          kwargs["username"] = schema.username
          kwargs["email"] = schema.email
          kwargs["is_verifed"] = schema.is_verifed
          kwargs["is_admin"] = schema.is_admin
          
     data = {
          "id": kwargs.get("id"),
          "username": kwargs.get("username"),
          "email": kwargs.get("email"),
          "is_verifed": kwargs.get("is_verifed"),
          "is_admin": kwargs.get("is_admin"),
          "exp": datetime.utcnow() + timedelta(minutes=60),
          "iat": datetime.utcnow()
     }
     encode = jwt.encode(data, key=settings.secret, algorithm=settings.alg)
     return TokenSchema(token=encode, type='bearer')



async def verify_token(token: str | None) -> TokenData:
     error = HTTPException(
          status_code=status.HTTP_401_UNAUTHORIZED,
          detail='Invalid token!'
     )
     if token is None:
          raise error
     try:
          payload = jwt.decode(token=token, key=settings.secret, algorithms=settings.alg)
          return TokenData(**payload)
          
     except JWTError:
          raise error