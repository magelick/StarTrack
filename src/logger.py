import logging
import sys

from src.settings import SETTINGS

# create logger
logger = logging.getLogger("app-logger")
# set logger level
logger.setLevel(level=SETTINGS.LOG_LEVEL)

# create formatter
formatter = logging.Formatter(
    fmt=SETTINGS.LOG_FORMAT,
)

# create stream handler and set level
stream_handler = logging.StreamHandler(stream=sys.stdout)
stream_handler.setFormatter(fmt=formatter)
# create file handler
file_handler = logging.FileHandler(filename="app.log")
file_handler.setFormatter(fmt=formatter)

# add handler into logger
logger.handlers = [stream_handler, file_handler]
