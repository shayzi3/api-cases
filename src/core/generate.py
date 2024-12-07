import random

from string import ascii_letters, ascii_uppercase, digits


def generate_id() -> str:
     password = ''
     symbols = ascii_letters + ascii_uppercase + digits
     
     for _ in range(10):
          password += random.choice(symbols)
     return password