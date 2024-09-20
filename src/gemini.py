from typing import AsyncGenerator

import google.generativeai as genai

from src.settings import SETTINGS

genai.configure(api_key=SETTINGS.GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-1.5-pro")


async def clean_and_format_text(text: str) -> str:
    """
    Function which formating created recommends
    :param text:
    :return:
    """
    # Удаление "##" и лишних пустых строк
    cleaned_text = text.replace("##", "").strip()

    # Убираем тройные переводы строк и заменяем на параграфы
    cleaned_text = cleaned_text.replace("\n\n\n", "</p><p>")

    # Форматируем списки
    cleaned_text = cleaned_text.replace("*", "<li>").replace(
        "\n\n", "<br><br>"
    )

    # Оборачиваем все в параграф
    cleaned_text = f"<p>{cleaned_text}</p>"
    return cleaned_text


async def generate_recommends(text: str) -> AsyncGenerator:
    """
    Function which create recommends for child
    :param text:
    :return:
    """
    data = await model.generate_content_async(text, stream=True)
    async for chunk in data:
        yield chunk.text


async def create_chat(message: str):
    """
    Function which create async chat
    :param message:
    :return:
    """
    chat = model.start_chat(history=[])
    response = await chat.send_message_async(content=message, stream=True)
    async for chunk in response:
        yield chunk.text
