from fastapi import APIRouter
from fastapi.responses import ORJSONResponse

from src.api.v1.router import router as v1_router
from src.api.auth.router import router as auth_router

# Initial api router
router = APIRouter(prefix="/api", default_response_class=ORJSONResponse)
# Include routers
router.include_router(router=v1_router)
router.include_router(router=auth_router)
