
from fastapi import Request, HTTPException, status
from src.schemas import TokenData
from src.core import verify_token



async def request_user_token(request: Request) -> TokenData:
     user = await verify_token(request.cookies.get("access_token"))
     return user


async def req_user_is_admin(request: Request) -> TokenData:
     user = await verify_token(request.cookies.get("access_token"))
     if user.is_admin is False:
          raise HTTPException(
               status_code=status.HTTP_403_FORBIDDEN, 
               detail="You are not an admin!"
          )
     return user