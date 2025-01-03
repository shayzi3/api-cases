import uvicorn

from fastapi import FastAPI, status

from src.schemas.api_v1 import ResponseModel

from src.api.api_v1.routers.items import (
     admin_items_router,
     items_router
)
from src.api.api_v1.routers.users import (
     admin_users_router,
     users_router
)
from src.api.api_v1.routers.verify import verify_router


app = FastAPI(
     title='Case API'
)
app.include_router(users_router)
app.include_router(verify_router)
app.include_router(items_router)
app.include_router(admin_items_router)
app.include_router(admin_users_router)


@app.get('/', response_model=ResponseModel)
async def root() -> ResponseModel:
     return ResponseModel(
          response='Ok', 
          status=status.HTTP_200_OK
     )


if __name__ == '__main__':
     uvicorn.run('main:app', reload=True)