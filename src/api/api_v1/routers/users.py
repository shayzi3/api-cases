from datetime import datetime, timedelta
from typing import Annotated
from fastapi import (
     APIRouter, 
     Depends, 
     HTTPException,
     Query, 
     status, 
     Response,
     UploadFile
)
from src.schemas import (
     UserSchema,
     RegisterUserSchema,
     RegisterUser,
     LoginUserSchema,
     ResponseModel,
     TokenData,
     UserWithPassword
)
from src.core.security import (
     verify_password, 
     create_token
)
from src.core import settings
from src.api.utils import UsersGetBy, valide_file
from src.db.bases import UserRepository
from src.schemas import TokenSchema
from src.api.dependencies import get_current_user
from src.services.redis import RedisPool
from src.services.storage3 import Storage3



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
     userdata = RegisterUser(**data)
     await UserRepository().create(**userdata)
     
     token = await create_token(**userdata)
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
     user_not_exists: UserWithPassword = await UserRepository().read_with_password(
          username=data.username
     )
     if user_not_exists is None:
          raise HTTPException(
               detail=f"Invalid username or password!",
               status_code=status.HTTP_403_FORBIDDEN
          )
     psw = verify_password(
          password=data.password,
          hashed_password=user_not_exists.password
     )
     if psw is False:
          raise HTTPException(
               detail="Invalid username or password!",
               status_code=status.HTTP_403_FORBIDDEN
          )
     token = await create_token(schema=user_not_exists)
     response.set_cookie(
          key="access_token",
          value=token,
          expires=(datetime.utcnow() + timedelta(minutes=60)).timestamp()
     )
     return token
     


@auth_router.delete("/out", response_model=ResponseModel)
async def out(
     response: Response,
     _: Annotated[TokenData, Depends(get_current_user)],
) -> ResponseModel:
     response.delete_cookie("access_token")
     return ResponseModel(
          response="Success!",
          status=status.HTTP_200_OK
     )
     
   

@auth_router.get("/", response_model=UserSchema)
async def get_user(
     current_user: Annotated[TokenData, Depends(get_current_user)],
     user_id: str = Query(default=None),
     username: str = Query(default=None),
) -> UserSchema:
     get_by = UsersGetBy().get_by(
          request_user_id=current_user.id,
          id=user_id,
          username=username
     )

     cached_user: str = await RedisPool().get(get_by.data_value)
     if cached_user:
          return UserSchema.convert_from_redis(cached_user)
     
     get_user = await UserRepository().read(**get_by.data)
     if get_user is None:
          raise HTTPException(
               detail="User not found!",
               status_code=status.HTTP_404_NOT_FOUND
          )
     await RedisPool().set(
          name=get_by.data_value,
          value=get_user.copy().convert_to_redis(),
          ex=110
     )
     return get_user



@auth_router.patch("/avatar", response_model=ResponseModel)
async def upload_avatar(
     current_user: Annotated[TokenData, Depends(get_current_user)],
     avatar: Annotated[UploadFile, Depends(valide_file)]
) -> ResponseModel:
     name = current_user.id + ".jpg"
     await Storage3.upload_file(
          file=avatar.file.read(),
          name=name
     )
     
     url_to_avatar = settings.s3_url + name
     await UserRepository().update(
          where={"id": current_user.id},
          avatar=url_to_avatar
     )
     
     return ResponseModel(
          response="Avatar Uploaded", 
          status=status.HTTP_200_OK
     )
     
     
@auth_router.patch("/change", response_model=ResponseModel)
async def user_change(
     current_user: Annotated[TokenData, Depends(get_current_user)],
) -> ResponseModel:
     
     raise NotImplementedError