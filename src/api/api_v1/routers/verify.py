
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import (
     APIRouter, 
     BackgroundTasks, 
     status,
     Body,
     Depends,
     HTTPException
)
from src.schemas import ResponseModel, TokenData
from src.services import (
     send_verification_code,
     check_verification_code
)
from src.db.base import user_orm
from src.db.models import get_db_session
from src.api.dependencies import check_verifed


verify_router = APIRouter(prefix="/api/v1/verify", tags=["Verify"])


@verify_router.post('/send', response_model=ResponseModel, description="Without code")
async def send_verify_code(
     data: Annotated[TokenData, Depends(check_verifed)],
     background_task: BackgroundTasks
) -> ResponseModel:
     background_task.add_task(
          send_verification_code,
          user_id=data.id,
          email=data.email,
          name=data.username
     )
     return ResponseModel(
          response="Code sended.",
          status=status.HTTP_200_OK
     )



@verify_router.post('/check', response_model=ResponseModel, description="With code")
async def check_verify_code(
     data: Annotated[TokenData, Depends(check_verifed)],
     code: Annotated[int, Body(embed=True)],
     session: Annotated[AsyncSession, Depends(get_db_session)]
) -> ResponseModel:
     result = await check_verification_code(
          user_id=data.id,
          code=code
     )
     if result is False:
          raise HTTPException(
               detail="Invalid code!",
               status_code=status.HTTP_400_BAD_REQUEST
          )
     await user_orm.update(
          session=session,
          where={"id": data.id},
          is_verifed=True
     )
     return ResponseModel(
          response="Account verified.",
          status=status.HTTP_200_OK
     )