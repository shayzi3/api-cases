from datetime import datetime, timedelta
from typing import Annotated, Any
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import (
     APIRouter, 
     Depends, 
     HTTPException, 
     status, 
     Response, 
     Request
)

from src.schemas import (
     UserSchema,
     RegisterUserSchema,
     RegisterUser,
     LoginUserSchema,
     ResponseModel
)
from src.db.models import get_db_session
from src.db import user_orm
from src.schemas import TokenSchema
from src.core import create_token, verify_password



auth_router = APIRouter(prefix="/api/v1/user", tags=["User"])


@auth_router.post("/signup", response_model=TokenSchema)
async def signup(
     data: RegisterUserSchema,
     session: Annotated[AsyncSession, Depends(get_db_session)],
     response: Response
) -> TokenSchema:
     user_exists: UserSchema = await user_orm.read(
          session=session,
          username=data.username
     )
     if user_exists:
          raise HTTPException(
               status_code=status.HTTP_403_FORBIDDEN,
               detail=f"User with nickname {data.username} already exists"
          )
     userdata = RegisterUser(**data.__dict__)
     await user_orm.create(
          session=session,
          **userdata.__dict__
     )
     token = await create_token(**userdata.__dict__)
     response.set_cookie(
          key="access_token", 
          value=token,
          expires=(datetime.utcnow() + timedelta(minutes=60)).timestamp()
     )
     return token
     
     
     
@auth_router.post("/login", response_model=TokenSchema)
async def login(
     data: LoginUserSchema,
     session: Annotated[AsyncSession, Depends(get_db_session)],
     response: Response
) -> TokenSchema:
     user_not_exists: list[Any] = await user_orm.read(
          session=session,
          values=('password', ),
          username=data.username
     )
     if user_not_exists is None:
          raise HTTPException(
               detail=f"Invalid username or password!",
               status_code=status.HTTP_403_FORBIDDEN
          )
     psw = verify_password(
          password=data.password,
          hashed_password=user_not_exists[0]
     )
     if psw is False:
          raise HTTPException(
               response="Invalid username or password!",
               status_code=status.HTTP_403_FORBIDDEN
          )
     token = await create_token(**user_not_exists.__dict__)
     response.set_cookie(
          key="access_token",
          value=token,
          expires=(datetime.utcnow() + timedelta(minutes=60)).timestamp()
     )
     return token
     


@auth_router.delete("/out", response_model=ResponseModel)
async def out(
     request: Request,
     response: Response
) -> ResponseModel:
     token = request.cookies.get("access_token")
     
     if token is None:
          raise HTTPException(
               detail="You unauthorized!",
               status_code=status.HTTP_401_UNAUTHORIZED
          )
     response.delete_cookie("access_token")
     return ResponseModel(
          response="Success!",
          status=status.HTTP_200_OK
     )
     
     

@auth_router.get("/", response_model=UserSchema)
async def get_user() -> UserSchema:
     return