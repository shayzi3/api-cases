import uvicorn

from fastapi import FastAPI, status

from src.schemas import ResponseModel
from src.api.api_v1.routers import (
     auth_router,
     verify_router,
     items_router
)


app = FastAPI(
     title='Case API'
)
app.include_router(auth_router)
app.include_router(verify_router)
app.include_router(items_router)


@app.get('/', response_model=ResponseModel)
async def root() -> ResponseModel:
     return ResponseModel(
          response='Hello!', 
          status=status.HTTP_200_OK
     )


if __name__ == '__main__':
     uvicorn.run('main:app', reload=True)