
import smtplib
import random

from email.mime.text import MIMEText
from loguru import logger
from src.core import settings
     


async def send_verification_code(user_id: str, email: str, name: str) -> None:
     
     code = random.randint(100000, 999999)
     msg = MIMEText(f"Your code is {code}")
     msg['Subject'] = "Verification code for CsCases.com"
     msg['From'] = "CsCases"
     msg['To'] = email

     try:
          with smtplib.SMTP_SSL('smtp.mail.ru', 465) as server:
               server.login(settings.email, settings.email_password)
               server.sendmail(settings.email, email, msg.as_string())
               logger.info(f"[MAIL INFO] send for {user_id}-{name} {(email)}")
     
     except Exception as ex:
          logger.error(f"[MAIL ERROR] {user_id}-{name} {(email, ex)}")
          
          
          
async def check_verification_code(user_id: str, name: str) -> bool:
     ...