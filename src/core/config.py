
from pydantic_settings import BaseSettings, SettingsConfigDict



class Settings(BaseSettings):
     postgres: str
     alg: str
     secret: str
     
     model_config = SettingsConfigDict(env_file='src/.env')
     
     
     
settings = Settings()