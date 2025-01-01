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
from src.api.dependencies import verify_current_user
from src.core.security import create_token


verify_router = APIRouter(prefix="/api/v1/verify", tags=["Verify"])


@verify_router.post('/send', response_model=ResponseModel)
async def send_verify_code(
     current_user: Annotated[TokenData, Depends(verify_current_user)],
     background_task: BackgroundTasks
) -> ResponseModel:
     already_send = await Email.user_already_send(current_user.id)
     if already_send is True:
          raise HTTPException(
               detail="You already send code! Wait 3 minutes",
               status_code=status.HTTP_408_REQUEST_TIMEOUT
          )
     
     background_task.add_task(
          Email.send_verification_code,
          user_id=current_user.id,
          email=current_user.email,
          name=current_user.username
     )
     return ResponseModel(
          response="Code sended.",
          status=status.HTTP_200_OK
     )



@verify_router.post('/check', response_model=ResponseModel)
async def check_verify_code(
     current_user: Annotated[TokenData, Depends(verify_current_user)],
     code: Annotated[str, Body(embed=True)],
     response: Response
) -> ResponseModel:
     result = await Email.check_verification_code(
          user_id=current_user.id,
          code=code
     )
     if result is False:
          raise HTTPException(
               detail="Invalid code!",
               status_code=status.HTTP_400_BAD_REQUEST
          )
     await UserRepository().update(
          where={"id": current_user.id},
          is_verifed=True
     )
     
     response.set_cookie(
          key="access_token",
          value=await create_token(**current_user.verify())
     )
     return ResponseModel(
          response="Account verified.",
          status=status.HTTP_200_OK
     )