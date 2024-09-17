from openai import AsyncOpenAI

from src.settings import SETTINGS

client = AsyncOpenAI(api_key=SETTINGS.OPENAI_API_KEY)


async def generate_recommend(prompt: str):
    response = await client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}], model="davinci-002"
    )
    return response
