from fastapi import APIRouter
from fastapi.responses import ORJSONResponse


# Initial child data router
router = APIRouter(
    prefix="/child_data",
    tags=["Child Data"],
    default_response_class=ORJSONResponse,
)
