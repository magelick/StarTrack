from fastapi import APIRouter
from fastapi.responses import ORJSONResponse

from src.api.v1.child import router as child_router

from src.api.v1.child_data import router as child_data_router

from src.api.v1.child_medical_data import router as child_medical_data_router
from src.api.v1.child_health_data import router as child_health_data_router
from src.api.v1.child_development_data import (
    router as child_development_data_router,
)
from src.api.v1.child_physical_data import router as child_physical_data_router
from src.api.v1.child_family_data import router as child_family_data_router
from src.api.v1.child_academic_data import router as child_academic_data_router
from src.api.v1.child_nutrition_data import (
    router as child_nutrition_data_router,
)

# Initial v1 router
router = APIRouter(prefix="/v1", default_response_class=ORJSONResponse)
# Including all routers
router.include_router(child_router)
router.include_router(child_data_router)
router.include_router(child_medical_data_router)
router.include_router(child_health_data_router)
router.include_router(child_development_data_router)
router.include_router(child_physical_data_router)
router.include_router(child_family_data_router)
router.include_router(child_academic_data_router)
router.include_router(child_nutrition_data_router)
