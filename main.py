from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis.asyncio import Redis

from src.settings import SETTINGS
from src.api.router import router as api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan func for application
    :param app:
    :return:
    """
    redis = Redis.from_url(
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
app.include_router(router=api_router)


if __name__ == "__main__":
    uvicorn.run(app="main:app", host="0.0.0.0", port=8000, reload=True)
