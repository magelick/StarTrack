from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis.asyncio import Redis
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from src.settings import SETTINGS
from src.api.router import router as api_router
from src.middlewares import MIDDLEWARES
from src.settings import templating
from src.logger import logger


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
    version="1.0.0",
    lifespan=lifespan,
)
# Include routers
app.include_router(router=api_router)
# Mount static files
app.mount(
    path="/static",
    app=StaticFiles(directory="./static"),
    name="static",
)

# Add all custom middlewares
for MIDDLEWARE, OPTIONS in MIDDLEWARES:
    app.add_middleware(MIDDLEWARE, **OPTIONS)


@app.get(path="/", response_class=HTMLResponse)
async def read_root(request: Request):
    try:
        return templating.TemplateResponse(
            "homepage.html", {"request": request}
        )
    except Exception as e:
        logger.error(e)


@app.get("/login", response_class=HTMLResponse)
async def login_template(request: Request):
    try:
        return templating.TemplateResponse("login.html", {"request": request})
    except Exception as e:
        logger.error(e)


@app.get(path="/ai_testing", response_class=HTMLResponse)
async def read_ai(request: Request):
    try:
        return templating.TemplateResponse(
            "ai_test.html", {"request": request}
        )
    except Exception as e:
        logger.error(e)


if __name__ == "__main__":
    uvicorn.run(app="main:app", host="0.0.0.0", port=8000, reload=True)
