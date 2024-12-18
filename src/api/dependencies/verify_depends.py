
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import status, Body, Depends, HTTPException
from src.core import verify_token
from src.db.models import get_db_session
from src.db.base import user_orm
from src.schemas import TokenData




async def check_verifed(
     token: Annotated[str, Body(embed=True)],
     session: Annotated[AsyncSession, Depends(get_db_session)]
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
     
     already_verifed = await user_orm.read(
          session=session,
          id=data.id
     )
     if already_verifed.is_verifed is True:
          raise HTTPException(
               detail="User already verifed!",
               status_code=status.HTTP_400_BAD_REQUEST
          )
     return data