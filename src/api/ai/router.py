from fastapi import APIRouter
from fastapi.responses import ORJSONResponse
from starlette import status

from src.gpt import generate_recommend

router = APIRouter(
    prefix="/ai", tags=["AI"], default_response_class=ORJSONResponse
)


@router.get(
    path="/recommends",
    status_code=status.HTTP_200_OK,
    name="Generate recommends",
)
async def get_recommends():
    prompt = "Сгенерируй рекомендации для развития ребёнка"
    data = await generate_recommend(prompt=prompt)
    return data
