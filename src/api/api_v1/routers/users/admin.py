
from typing import Annotated
from fastapi import APIRouter, Depends, status, Query
from src.schemas.api_v1 import ResponseModel, TokenData
from src.api.api_v1.dependencies import current_user_is_admin



admin_users_router = APIRouter(prefix="/api/v1/admin/user", tags=["User Admin"])



@admin_users_router.patch("/ban", response_model=ResponseModel)
async def admin_ban_user(
     current_user: Annotated[TokenData, Depends(current_user_is_admin)],
     user_id: str = Query()
) -> ResponseModel:
     
     
     return ResponseModel(
          response="Success ban user",
          status=status.HTTP_200_OK
     )
     

@admin_users_router.delete("/delete", response_model=ResponseModel)
async def admin_delete_user(
     current_user: Annotated[TokenData, Depends(current_user_is_admin)],
     user_id: str = Query()
) -> ResponseModel:
     
     
     return ResponseModel(
          response="Success ban user",
          status=status.HTTP_200_OK
     )
     
     
@admin_users_router.patch("/change", response_model=ResponseModel)
async def admin_change_user(
     current_user: Annotated[TokenData, Depends(current_user_is_admin)],
     
) -> ResponseModel:
     
     
     return ResponseModel(
          response="Success ban user",
          status=status.HTTP_200_OK
     )
