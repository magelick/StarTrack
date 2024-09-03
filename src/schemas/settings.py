from dotenv import load_dotenv
from pydantic import RedisDsn
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    """
    Base settings schema
    """

    AIOREDIS_URL: RedisDsn
