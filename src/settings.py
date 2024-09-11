from pathlib import Path

from passlib.context import CryptContext
from starlette.templating import Jinja2Templates

from src.schemas.settings import Settings

# Base path to app
BASE_DIR = Path(__file__).resolve().parent.parent
# Initial Base settings schema instance
SETTINGS = Settings()  # type: ignore
# Initial pwd context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# Mount templates
templating = Jinja2Templates(directory="templates")
