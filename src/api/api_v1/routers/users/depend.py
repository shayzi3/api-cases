from fastapi import UploadFile, HTTPException, status


async def valide_file(file: UploadFile) -> UploadFile:
     if file.filename.split(".")[-1] not in ["jpg", "png"]:
          raise HTTPException(
               detail="File must be jpg or png!",
               status_code=status.HTTP_403_FORBIDDEN
          )
     return file