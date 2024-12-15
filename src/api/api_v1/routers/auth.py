from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks

from src.schemas import (
     UserSchema,
     RegisterUserSchema,
     RegisterUser,
     LoginUserSchema
)

from src.db.models import get_db_session
from src.db import user_orm
from src.schemas import TokenSchema
from src.core import create_token, hashed_password


auth_router = APIRouter(prefix='/api/v1/user', tags=['User'])


@auth_router.post('/signup', response_model=TokenSchema)
async def signup(
     data: RegisterUserSchema,
     session: Annotated[AsyncSession, Depends(get_db_session)],
) -> TokenSchema:
     userdata = RegisterUser(**data.__dict__)
     
     user_exists = await user_orm.read(
          session=session,
          username=userdata.username
     )
     if user_exists:
          raise HTTPException(
               status_code=status.HTTP_403_FORBIDDEN,
               detail=f'User with nickname {userdata.username} already exists'
          )
     userdata.password = await hashed_password(userdata.password)
     await user_orm.create(
          session=session,
          **userdata.__dict__
     )
     return await create_token(**userdata.__dict__)
     
     
     
@auth_router.post('/login', response_model=TokenSchema)
async def login(
     data: LoginUserSchema

) -> TokenSchema:
     return
     
     

@auth_router.get('/', response_model=UserSchema)
async def get_user() -> UserSchema:
     return