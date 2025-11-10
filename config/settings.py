from pydantic import Field
from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv
load_dotenv()

class Settings(BaseSettings):
    DB_URL: str = Field(default=os.getenv("DB_URL"))


settings = Settings()