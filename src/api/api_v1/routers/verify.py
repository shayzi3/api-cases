
from typing import Annotated
from fastapi import (
     APIRouter, 
     Depends, 
     BackgroundTasks, 
     status,
     HTTPException
)
from src.schemas import ResponseModel, VerifyData, TokenData
from src.services import (
     send_verification_code,
     check_verification_code
)
from src.core import verify_token
from src.api.dependencies import check_verifed


verify_router = APIRouter(prefix="/api/v1/verify", tags=["Verify"])


@verify_router.post('/send', response_model=ResponseModel, description="Without code")
async def send_verify_code(
     data: Annotated[TokenData, Depends(check_verifed)],
     background_task: BackgroundTasks
) -> ResponseModel:
     if isinstance(data, ResponseModel):
          return data
     
     elif isinstance(data, VerifyData):
          return ResponseModel(
               response="For endpoind /send no code needed",
               status=status.HTTP_400_BAD_REQUEST
          )
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
     data: Annotated[VerifyData, Depends(check_verifed)]
) -> ResponseModel:
     if isinstance(data, ResponseModel):
          return data
     
     elif isinstance(data, TokenData):
          return ResponseModel(
               response="For endpoint /check code needed",
               status=status.HTTP_400_BAD_REQUEST
          )
     # await check_verification_code