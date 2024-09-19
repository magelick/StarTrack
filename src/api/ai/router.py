from fastapi import APIRouter, WebSocket
from fastapi.responses import ORJSONResponse

from src.gemini import generate_recommends, clean_and_format_text

router = APIRouter(
    prefix="/ai", tags=["AI"], default_response_class=ORJSONResponse
)


@router.websocket(
    path="/recommends",
    name="Generate recommends",
)
async def get_recommends(websocket: WebSocket):
    await websocket.accept()
    text = """
    Проанализируй эти данные о ребенке и напиши меню на неделю для всей семьи с указанием  рецептов, количества ингредиентов и времени. Составь список продуктов, которые нужно купить с указанием количества, а также выведи сумму затрат на покупки в валюте локации: 12 лет; пол: мужской; рост: 150; вес: 60; ИМТ: не нужно; аллергии: цитрусовые; особенности питания и предпочтения: не любит грибы; хронические заболевания: диабет; локация: Беларусь; сезон: осень. Пример вывода информации:
Понедельник
Завтрак
«Контент»
Ингредиенты
Рецепт
Время приготовления
Блюдо ребёнка
Фото блюд
Обед
«Контент»
Ингредиенты
Рецепт
Время приготовления
Блюдо ребёнка
Фото блюд
Ужин
«Контент»
Ингредиенты
Рецепт
Время приготовления
Блюдо ребёнка
Фото блюд
Также для вторника - воскресенья.
    """
    async for chunk in generate_recommends(text=text):  # type: ignore
        await websocket.send_text(await clean_and_format_text(chunk))

    await websocket.close()
