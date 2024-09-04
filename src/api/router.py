from fastapi import APIRouter
from fastapi.responses import ORJSONResponse

from src.api.v1.router import router as v1_router

# Initial api router
router = APIRouter(prefix="/api", default_response_class=ORJSONResponse)
# Include v1 router
router.include_router(router=v1_router)
