from fastapi import APIRouter
from fastapi.responses import ORJSONResponse

from src.api.v1.child import router as child_router


# Initial v1 router
router = APIRouter(
    prefix="/v1",
    default_response_class=ORJSONResponse,
)
# Including all routers
router.include_router(child_router)
