
from fastapi import status
from src.core import verify_token
from src.schemas import ResponseModel, TokenData, VerifyData




async def check_verifed(
     verify_data: VerifyData
) -> TokenData | VerifyData:
     """Функция проверяет валидность токена и верифицикацию пользователя.
     
     Args:
          verify_data - pydantic model: 
               token: str
               code: int | None
     
     Returns:
          Если code не был передан значит использовали эндпоинт /send -> TokenData
          Если code был передан значит использовали эндпоинт /verify -> VerifyData
     """
     token_data = await verify_token(verify_data.token)

     if token_data.is_verifed is True:
          return ResponseModel(
               response="Account already verified",
               status=status.HTTP_400_BAD_REQUEST
          )
     if verify_data.code == 0:
          return token_data
     return verify_data