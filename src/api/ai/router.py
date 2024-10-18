from fastapi import APIRouter, WebSocket
from fastapi.responses import ORJSONResponse
from src.gemini import generate_recommends, clean_and_format_text
from src.logger import logger

router = APIRouter(
    prefix="/ai",
    tags=["AI"],
    default_response_class=ORJSONResponse,
)


@router.websocket(
    path="/recommends",
    name="Generate recommends",
)
async def get_recommends(websocket: WebSocket):
    try:
        await websocket.accept()
        text = """
        Проанализируй эти данные о ребенке и напиши меню на неделю для всей семьи с указанием рецептов,
        количества ингредиентов и времени: 12 лет; пол: мужской; рост: 150; вес: 60; ИМТ: не нужно;
        аллергии: цитрусовые; особенности питания и предпочтения: не любит грибы; хронические заболевания: нет.
        Составь список продуктов, которые нужно купить с указанием количества. Обязательно учитывай то,
        что страна (регион) - Беларусь.
        Пример вывода информации:

        Понедельник
            Завтрак
                Ингредиенты
                Рецепт (способ приготовления)
                Время приготовления

            Обед
                Ингредиенты
                Рецепт (способ приготовления)
                Время приготовления

            Ужин
                Ингредиенты
                Рецепт (способ приготовления)
                Время приготовления

        Также для всех оставшихся дней недели.
        """
        async for chunk in generate_recommends(text=text):  # type: ignore
            await websocket.send_text(await clean_and_format_text(chunk))
    except Exception as e:
        logger.error(msg=e)
    finally:
        await websocket.close()
