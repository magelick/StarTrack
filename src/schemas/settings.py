from dotenv import load_dotenv
from pydantic import RedisDsn, PostgresDsn
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    """
    Base settings schema
    """

    DATABASE_URL: PostgresDsn
    AIOREDIS_URL: RedisDsn
