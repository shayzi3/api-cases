from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
     # Postgres
     postgres: str
     
     #Jwt
     alg: str
     secret: str
     
     # Mail.ru
     email: str 
     email_password: str
     
     # S3
     s3_access_key: str
     s3_secret_key: str
     s3_endpoint_url: str
     s3_bucket_name: str
     s3_url: str
     
     model_config = SettingsConfigDict(env_file='src/.env')
     
     
     
settings = Settings()