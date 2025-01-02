from datetime import datetime, timedelta
from typing import Annotated
from fastapi import (
     APIRouter,
     Body, 
     Depends,
     HTTPException,
     Query, 
     status, 
     Response,
     UploadFile,
     BackgroundTasks
)
from src.schemas import (
     UserSchema,
     RegisterUserSchema,
     RegisterUser,
     LoginUserSchema,
     ResponseModel,
     TokenData,
     UserWithPassword,
     UserBodyNullable
)
from src.core.security import (
     verify_password, 
     create_token,
     hashed_password
)
from src.api.utils import (
     UsersGetBy, 
     valide_file, 
     background_upload_avatar,
     background_delete_avatar
)
from src.db.bases import UserRepository
from src.schemas import TokenSchema
from src.api.dependencies import get_current_user
from src.services.redis import RedisPool



users_router = APIRouter(prefix="/api/v1/user", tags=["User"])



@users_router.post("/signup", response_model=TokenSchema)
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
     
     

@users_router.post("/login", response_model=TokenSchema)
async def login(
     data: LoginUserSchema,
     response: Response
) -> TokenSchema:
     user_not_exists = await UserRepository().read_with_password(
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
     


@users_router.delete("/out", response_model=ResponseModel)
async def out(
     response: Response,
     _: Annotated[TokenData, Depends(get_current_user)],
) -> ResponseModel:
     response.delete_cookie("access_token")
     return ResponseModel(
          response="Success!",
          status=status.HTTP_200_OK
     )
     
   

@users_router.get("/", response_model=UserSchema)
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



@users_router.patch("/avatar", response_model=ResponseModel)
async def upload_avatar(
     current_user: Annotated[TokenData, Depends(get_current_user)],
     avatar: Annotated[UploadFile, Depends(valide_file)],
     background_task: BackgroundTasks
) -> ResponseModel:
     filename = current_user.id + ".jpg"
     
     background_task.add_task(
          background_upload_avatar,
          file=avatar.file.read(),
          filename=filename,
          user_id=current_user.id,
          redis_values=current_user.redis_values
     )
     return ResponseModel(
          response="Avatar Uploaded", 
          status=status.HTTP_200_OK
     )
     
     
     
@users_router.delete("/avatar", response_model=ResponseModel)
async def delete_avatar(
     current_user: Annotated[TokenData, Depends(get_current_user)],
     background_task: BackgroundTasks
) -> ResponseModel:
     filename = current_user.id + ".jpg"
     
     background_task.add_task(
          background_delete_avatar,
          filename=filename,
          user_id=current_user.id,
          redis_values=current_user.redis_values
     )
     return ResponseModel(
          response="Avatar Deleted",
          status=status.HTTP_200_OK
     )
     
     
     
@users_router.patch("/", response_model=ResponseModel)
async def user_change(
     current_user: Annotated[TokenData, Depends(get_current_user)],
     data: UserBodyNullable
) -> ResponseModel:
     await UserRepository().update(
          where={"id": current_user.id},
          redis_value=current_user.redis_values,
          **data.not_nullable
     )
     return ResponseModel(
          response="User Updated",
          status=status.HTTP_200_OK
     )
     
     
@users_router.patch("/password", response_model=ResponseModel)
async def user_change_password(
     current_user: Annotated[TokenData, Depends(get_current_user)],
     old_password: Annotated[str, Body(embed=True)],
     new_password: Annotated[str, Body(embed=True)]
) -> ResponseModel:
     user_password = await UserRepository().read_with_password(
          id=current_user.id
     )
     
     psw = verify_password(
          password=old_password,
          hashed_password=user_password.password
     )
     if psw is False:
          raise HTTPException(
               detail="Invalid password!",
               status_code=status.HTTP_403_FORBIDDEN
          )
          
     await UserRepository().update(
          where={"id": current_user.id},
          redis_value=current_user.redis_values,
          password=hashed_password(new_password)
     )
     return ResponseModel(
          response="Password Change",
          status=status.HTTP_200_OK
     )