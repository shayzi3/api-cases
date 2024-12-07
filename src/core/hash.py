import bcrypt


async def hashed_password(password: str) -> str:
     return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
     
     
async def verify_password(password: str, hashed_password: str) -> bool:
     return bcrypt.checkpw(password.encode(), hashed_password.encode())