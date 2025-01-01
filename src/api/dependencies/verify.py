
from typing import Annotated
from fastapi import status, Body, HTTPException
from src.core.security import verify_token
from src.schemas import TokenData
from src.db.bases import UserRepository



async def verify_current_user(
     token: Annotated[str, Body(embed=True)],
) -> TokenData:
     """Function check the validity of the token. 
     Also check for re-verification

     Args:
         session (Annotated[AsyncSession, Depends): AsyncSession
         token (Annotated[str, Body, optional): jwt token

     Returns:
         TokenData
     """
     data = await verify_token(token)
     if data.is_verifed is True:
          raise HTTPException(
               detail="User already verifed!",
               status_code=status.HTTP_400_BAD_REQUEST
          )
     return data