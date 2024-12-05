
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends

from src.schemas import UserSchema
from .schema import (
     RegisterUserSchema,
     RegisterUser,
     LoginUserSchema
)
from src.db.models import get_db_session


auth_router = APIRouter(prefix='/api/v1/user', tags=['User'])


@auth_router.post('/register', response_model=UserSchema)
async def register(
     data: RegisterUserSchema,
     session: Annotated[AsyncSession, Depends(get_db_session)]
) -> UserSchema:
     user = RegisterUser(**data.__dict__)
     
     return UserSchema(**user.__dict__)
     
     
@auth_router.post('/auth', response_model=UserSchema)
async def auth(
     data: LoginUserSchema

) -> UserSchema:
     return
     

@auth_router.get('/', response_model=UserSchema)
async def get_user() -> UserSchema:
     return