from pathlib import Path
from src.schemas.settings import Settings

# Base path to app
BASE_DIR = Path(__file__).resolve().parent.parent
# Initial Base settings schema instance
SETTINGS = Settings()
