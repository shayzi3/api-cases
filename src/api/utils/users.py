from fastapi import UploadFile, HTTPException, status, File


async def get_by_id_username(
     request_user_id: str,
     id: str | None = None,
     username: str | None = None,
) -> dict[str, str]:
     get_by = {"username": username} if username else {"id": id}
     
     if (id is None) and (username is None):
          get_by = {"id": request_user_id}
     return get_by


async def valide_file(file: UploadFile) -> UploadFile:
     if file.filename.split(".")[-1] not in ["jpg", "png"]:
          raise HTTPException(
               detail="File must be jpg or png!",
               status_code=status.HTTP_403_FORBIDDEN
          )
     return file


