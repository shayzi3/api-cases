from typing import Annotated
from fastapi import (
     APIRouter,
     Depends,
     HTTPException,
     status,
)
from src.db.api_v1.bases import ItemRepository
from src.schemas.api_v1 import TokenData, ResponseModel
from src.api.api_v1.dependencies import current_user_is_admin

from .schema import ItemBody, ItemBodyID, ItemBodyNullable



admin_items_router = APIRouter(prefix="/api/v1/admin/item", tags=["Item Admin"])


     
@admin_items_router.post(path='/create', response_model=ItemBodyID)
async def create_item(
     _: Annotated[TokenData, Depends(current_user_is_admin)],
     item: ItemBody
) -> ItemBodyID:
     item_exists = await ItemRepository().read(
          name=item.name,
          quality=item.quality
     )
     if item_exists is not None:
          raise HTTPException(
               status_code=status.HTTP_409_CONFLICT, 
               detail="Item already exists"
          )
     
     item_data = ItemBodyID(**item.__dict__)
     await ItemRepository().create(**item_data.__dict__)
     
     return item_data
     


@admin_items_router.patch(path='/change', response_model=ResponseModel)
async def change_item(
     _: Annotated[TokenData, Depends(current_user_is_admin)],
     item_id: str,
     item: ItemBodyNullable
) -> ResponseModel:
     item_exists = await ItemRepository().read(id=item_id)
     if item_exists is None:
          raise HTTPException(
               status_code=status.HTTP_404_NOT_FOUND, 
               detail="Item not found!"
          )
          
     await ItemRepository().update(
          where={"id": item_id},
          redis_value=item_exists.redis_values,
          **item.not_nullable
     )
     return ResponseModel(
          response="Item updated!",
          status=status.HTTP_200_OK
     )