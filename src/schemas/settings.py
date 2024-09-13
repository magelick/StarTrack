from dotenv import load_dotenv
from pydantic import RedisDsn, PostgresDsn, SecretStr
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    """
    Base settings schema
    """

    DATABASE_URL: PostgresDsn
    AIOREDIS_URL: RedisDsn
    SECRET_KEY_OF_ACCESS_TOKEN: SecretStr
    SECRET_KEY_OF_REFRESH_TOKEN: SecretStr
    ACCESS_TOKEN_EXPIRE: int
    REFRESH_TOKEN_EXPIRE: int
    ALGORITHM: str
    TOKEN_TYPE: str
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(levelname)s  %(asctime)s | %(message)s"
