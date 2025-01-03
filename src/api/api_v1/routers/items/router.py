from typing import Annotated
from fastapi import (
     APIRouter,
     Depends,
     HTTPException,
     status,
     Query
)
from src.db.api_v1.bases import ItemRepository
from src.services.redis import RedisPool
from src.schemas.api_v1 import TokenData, ItemSchema
from src.api.api_v1.dependencies import get_current_user

from .util import ItemsGetBy


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