
import smtplib
import random

from email.mime.text import MIMEText
from loguru import logger
from src.core import settings
from src.core import Stack


async def send_verification_code(user_id: str, email: str, name: str) -> None:
     stack = Stack()
     code = random.randint(100000, 999999)
     msg = MIMEText(f"Your code is {code}")
     msg["Subject"] = "Verification code"
     msg["From"] = settings.email
     msg["To"] = email

     try:
          with smtplib.SMTP_SSL('smtp.mail.ru', 465) as server:
               server.login(settings.email, settings.email_password)
               server.sendmail(settings.email, email, msg.as_string())
               stack.set(user_id, code)
               logger.info(f"[MAIL INFO] send for {user_id}-{name} {(email)}")
     
     except Exception as ex:
          logger.error(f"[MAIL ERROR] {user_id}-{name} {(email, ex)}")
          
          
          
async def check_verification_code(user_id: int, code: int) -> bool:
     stack = Stack()
     if stack.get(user_id) == code:
          stack.delete(user_id)
          return True
     return False
     
     