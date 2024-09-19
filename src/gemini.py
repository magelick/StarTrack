from typing import AsyncGenerator

import google.generativeai as genai

from src.settings import SETTINGS

genai.configure(api_key=SETTINGS.GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-1.5-flash")


async def clean_and_format_text(text: str) -> str:
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
    data = await model.generate_content_async(text, stream=True)
    async for chunk in data:
        yield chunk.text
