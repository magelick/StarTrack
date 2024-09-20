from fastapi import APIRouter, WebSocket
from fastapi.responses import ORJSONResponse
from starlette.websockets import WebSocketDisconnect

from src.dependencies import ChatSession, ConnectionManager
from src.gemini import generate_recommends, clean_and_format_text, create_chat

router = APIRouter(
    prefix="/ai",
    tags=["AI FUNCTIONALITY"],
    default_response_class=ORJSONResponse,
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


@router.websocket(path="/chat", name="Create Chat with Gemini AI")
async def chat_ai(
    websocket: WebSocket, manager: ConnectionManager = ChatSession
):
    """

    :param websocket:
    :param manager:
    :return:
    """
    # Подключение пользователя
    await manager.connect(websocket)
    try:
        while True:
            # Ожидание сообщения от клиента
            data = await websocket.receive_text()

            # Отправка запроса к Gemini AI
            ai_response_generator = create_chat(data)

            # Получаем ответы по частям и отправляем клиенту через WebSocket
            async for chunk in ai_response_generator:
                await manager.send_personal_message(chunk, websocket)
    except WebSocketDisconnect:
        # Отключение пользователя
        manager.disconnect(websocket)
