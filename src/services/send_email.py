import smtplib
import random

from email.mime.text import MIMEText
from loguru import logger
from src.core import settings
from src.services.redis import RedisPool



class Email:
     redis = RedisPool()
     
     
     @classmethod
     async def user_already_send(cls, user_id: str) -> bool:
          # True - user in redis
          # False - user not in redis
          return await cls.redis.exists(f"code:{user_id}") == 1
     
     
     @classmethod
     async def send_verification_code(cls, user_id: str, email: str, name: str) -> None:
          code = random.randint(100000, 999999)
          msg = MIMEText(f"Your code is {code}")
          msg["Subject"] = "Verification code"
          msg["From"] = settings.email
          msg["To"] = email

          try:
               with smtplib.SMTP_SSL('smtp.mail.ru', 465) as server:
                    server.login(settings.email, settings.email_password)
                    server.sendmail(settings.email, email, msg.as_string())
                    logger.info(f"[MAIL INFO] send for {user_id}-{name} {(email)}")
                    
                    await cls.redis.set(name=f"code:{user_id}", value=code, ex=180)
          
          except Exception as ex:
               logger.error(f"[MAIL ERROR] {user_id}-{name} {(email, ex)}")
               
               
     @classmethod
     async def check_verification_code(cls, user_id: str, code: str) -> bool:
          value: bytes = await cls.redis.get(f"code:{user_id}")
          return value.decode() == code
     
     