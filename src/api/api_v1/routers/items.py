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
     ItemBodyID
)
from src.api.dependencies import (
     request_user_token,
     req_user_is_admin
)
from src.db.bases import ItemRepository


items_router = APIRouter(prefix="/api/v1/item", tags=["Item"])
     


@items_router.get(path='/', response_model=ItemSchema)
async def get_item(
     _: Annotated[TokenData, Depends(request_user_token)],
     item_id: int = Query(default=None),
     item_name: str = Query(default=None),
) -> ItemSchema:
     ...
     
     
@items_router.post(path='/', response_model=ItemBodyID, tags=["Item Admin"])
async def create_item(
     _: Annotated[TokenData, Depends(req_user_is_admin)],
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
     
     
@items_router.patch(path='/', response_model=ResponseModel, tags=["Item Admin"])
async def change_item(
     _: Annotated[TokenData, Depends(req_user_is_admin)],
     item_id: int,
     item: ItemBody
) -> ResponseModel:
     ...