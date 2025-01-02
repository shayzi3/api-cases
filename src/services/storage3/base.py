from contextlib import asynccontextmanager
from aiobotocore.session import get_session, AioBaseClient
from typing import AsyncGenerator

from src.core import settings



class Storage3:
     access_key = settings.s3_access_key
     secret_key = settings.s3_secret_key
     endpoint_url = settings.s3_endpoint_url
     bucket_name = settings.s3_bucket_name
     
     session = get_session()
     
     config = {
          "aws_access_key_id": access_key,
          "aws_secret_access_key": secret_key,
          "endpoint_url": endpoint_url,
          "verify": False
     }
     
     
     @classmethod
     @asynccontextmanager
     async def get_client(cls) -> AsyncGenerator[AioBaseClient, None]:
          async with cls.session.create_client("s3", **cls.config) as client:
               yield client
               
               
     @classmethod
     async def upload_file(cls, file: bytes, name: str) -> None:
          async with cls.get_client() as client:
               await client.put_object(
                    Bucket=cls.bucket_name,
                    Key=name,
                    Body=file
               )
              
     @classmethod
     async def delete_file(cls, name: str) -> None:
          async with cls.get_client() as client:
               await client.delete_object(
                    Bucket=cls.bucket_name,
                    Key=name
               )
               
               
     
          
     