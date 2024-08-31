from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

# Create FastAPI app
app = FastAPI(
    title="StarTrack",
    summary="",
    description="",
    default_response_class=ORJSONResponse,
)
