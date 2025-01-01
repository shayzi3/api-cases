from typing import Annotated
from fastapi import (
     APIRouter,
     Depends,
     HTTPException,
     status,
     Query
)
from src.schemas import (
     TokenData,
     ItemSchema,
     ResponseModel,
     ItemBody,
     ItemBodyID,
     ItemBodyNullable
)
from src.api.dependencies import (
     get_current_user,
     current_user_is_admin
)
from src.api.utils import ItemsGetBy
from src.db.bases import ItemRepository
from src.services.redis import RedisPool


items_router = APIRouter(prefix="/api/v1/item", tags=["Item"])
     


@items_router.get(path='/', response_model=ItemSchema)
async def get_item(
     _: Annotated[TokenData, Depends(get_current_user)],
     item_id: str = Query(default=None),
     item_name: str = Query(default=None),
) -> ItemSchema:
     get_by = ItemsGetBy().get_by(item_id, item_name)
     
     cached_item = await RedisPool().get(get_by.data_value)
     if cached_item is not None:
          return ItemSchema.convert_from_redis(cached_item)
     
     item = await ItemRepository().read(**get_by.data)
     if item is None:
          raise HTTPException(
               detail="Item not found!",
               status_code=status.HTTP_404_NOT_FOUND
          )
     await RedisPool().set(
          name=get_by.data_value,
          value=item.copy().convert_to_redis(),
          ex=110
     )
     return item
     
     
@items_router.post(path='/', response_model=ItemBodyID, tags=["Admin"])
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
     


@items_router.patch(path='/', response_model=ResponseModel, tags=["Admin"])
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
          
     args = [f"item:{item_exists.id}", f"item:{item_exists.name}"]
     await ItemRepository().update(
          where={"id": item_id},
          redis_value=args,
          **item.not_nullable
     )
     return ResponseModel(
          response="Item updated!",
          status=status.HTTP_200_OK
     )