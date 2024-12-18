from datetime import timedelta, datetime
from fastapi import HTTPException, status
from jose import jwt, JWTError

from src.schemas import TokenSchema, TokenData
from src.core import settings


async def create_token(*args, **kwargs) -> TokenSchema:
     if args:
          kwargs["id"] = args[0]
          kwargs["username"] = args[1]
          kwargs["email"] = args[2]
          kwargs["is_verifed"] = args[3]
          
     data = {
          "id": kwargs.get("id"),
          "username": kwargs.get("username"),
          "email": kwargs.get("email"),
          "is_verifed": kwargs.get("is_verifed")
     }
     data.update(
          {
               'exp': datetime.utcnow() + timedelta(minutes=60),
               'iat': datetime.utcnow()
          }
     )
     encode = jwt.encode(data, key=settings.secret, algorithm=settings.alg)
     return TokenSchema(token=encode, type='bearer')


async def verify_token(token: str) -> TokenData:
     try:
          payload = jwt.decode(token=token, key=settings.secret, algorithms=settings.alg)
          return TokenData(**payload)
          
     except JWTError:
          raise HTTPException(
               status_code=status.HTTP_401_UNAUTHORIZED,
               detail='Invalid token!'
          )