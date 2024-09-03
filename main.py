from contextlib import asynccontextmanager

import aioredis
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from src.settings import SETTINGS


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan func for application
    :param app:
    :return:
    """
    redis = aioredis.from_url(
        SETTINGS.AIOREDIS_URL.unicode_string(),
        max_connections=20,
        encoding="utf8",
        decode_responses=True,
        socket_connect_timeout=5,
        socket_timeout=5,
    )
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache", expire=60)
    yield


# Create FastAPI app
app = FastAPI(
    title="StarTrack",
    summary="",
    description="",
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
)
