from src.schemas.base import DTO
from src.settings import SETTINGS


class TokenData(DTO):
    access_token: str
    refresh_token: str
    token_type: str = SETTINGS.TOKEN_TYPE
