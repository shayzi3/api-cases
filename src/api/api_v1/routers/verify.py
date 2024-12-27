from typing import Annotated
from fastapi import (
     APIRouter, 
     BackgroundTasks, 
     status,
     Body,
     Depends,
     HTTPException,
     Response
)
from src.schemas import ResponseModel, TokenData
from src.services import Email
from src.db.bases import UserRepository
from src.api.dependencies import check_verifed
from src.core.security import create_token


verify_router = APIRouter(prefix="/api/v1/verify", tags=["Verify"])


@verify_router.post('/send', response_model=ResponseModel)
async def send_verify_code(
     data: Annotated[TokenData, Depends(check_verifed)],
     background_task: BackgroundTasks
) -> ResponseModel:
     already_send = await Email.user_already_send(data.id)
     if already_send is True:
          raise HTTPException(
               detail="You already send code! Wait 3 minutes",
               status_code=status.HTTP_408_REQUEST_TIMEOUT
          )
     
     background_task.add_task(
          Email.send_verification_code,
          user_id=data.id,
          email=data.email,
          name=data.username
     )
     return ResponseModel(
          response="Code sended.",
          status=status.HTTP_200_OK
     )



@verify_router.post('/check', response_model=ResponseModel)
async def check_verify_code(
     data: Annotated[TokenData, Depends(check_verifed)],
     code: Annotated[str, Body(embed=True)],
     response: Response
) -> ResponseModel:
     result = await Email.check_verification_code(
          user_id=data.id,
          code=code
     )
     if result is False:
          raise HTTPException(
               detail="Invalid code!",
               status_code=status.HTTP_400_BAD_REQUEST
          )
     await UserRepository().update(
          where={"id": data.id},
          is_verifed=True
     )
     
     response.set_cookie(
          key="access_token",
          value=await create_token(**data.verify())
     )
     return ResponseModel(
          response="Account verified.",
          status=status.HTTP_200_OK
     )