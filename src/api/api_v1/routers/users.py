from datetime import datetime, timedelta
from typing import Annotated, Any
from fastapi import (
     APIRouter, 
     Depends, 
     HTTPException,
     Query, 
     status, 
     Response, 
)
from src.schemas import (
     UserSchema,
     RegisterUserSchema,
     RegisterUser,
     LoginUserSchema,
     ResponseModel,
     TokenData
)
from src.core.security import (
     verify_password, 
     create_token
)
from src.api.utils import get_by_id_username
from src.db.bases import UserRepository
from src.schemas import TokenSchema
from src.api.dependencies import request_user_token
from src.services.redis import RedisPool



auth_router = APIRouter(prefix="/api/v1/user", tags=["User"])



@auth_router.post("/signup", response_model=TokenSchema)
async def signup(
     data: RegisterUserSchema,
     response: Response
) -> TokenSchema:
     user_exists = await UserRepository().read(
          username=data.username
     )
     if user_exists is not None:
          raise HTTPException(
               status_code=status.HTTP_403_FORBIDDEN,
               detail=f"User with nickname {data.username} already exists"
          )
     userdata = RegisterUser(**data.__dict__)
     await UserRepository().create(
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
     response: Response
) -> TokenSchema:
     user_not_exists: list[Any] = await UserRepository().read(
          values=("password", "id", "username", "email", "is_verifed", "is_admin"),
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
               detail="Invalid username or password!",
               status_code=status.HTTP_403_FORBIDDEN
          )
     token = await create_token(*user_not_exists[1:])
     response.set_cookie(
          key="access_token",
          value=token,
          expires=(datetime.utcnow() + timedelta(minutes=60)).timestamp()
     )
     return token
     


@auth_router.delete("/out", response_model=ResponseModel)
async def out(
     response: Response,
     _: Annotated[TokenData, Depends(request_user_token)],
) -> ResponseModel:
     response.delete_cookie("access_token")
     return ResponseModel(
          response="Success!",
          status=status.HTTP_200_OK
     )
     
   

@auth_router.get("/", response_model=UserSchema)
async def get_user(
     request_user: Annotated[TokenData, Depends(request_user_token)],
     user_id: str = Query(default=None),
     username: str = Query(default=None),
) -> UserSchema:
     get_by = await get_by_id_username(
          request_user_id=request_user.id,
          id=user_id,
          username=username
     )
     cached_user: str = await RedisPool().get(list(get_by.values())[0])
     if cached_user:
          return UserSchema.convert_from_redis(cached_user)
     
     get_user = await UserRepository().read(**get_by)
     if get_user is None:
          raise HTTPException(
               detail="User not found!",
               status_code=status.HTTP_404_NOT_FOUND
          )
          
     await RedisPool().set(
          name=list(get_by.values())[0],
          value=get_user.copy().convert_to_redis(),
          ex=200
     )
     return get_user
     