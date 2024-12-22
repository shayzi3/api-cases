from pydantic import BaseModel



class VerifyData(BaseModel):
     token: str
     code: int | None = None