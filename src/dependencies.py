from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Base


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Depend,which create session to database
    :return:
    """
    async with Base.async_session_maker() as session:
        yield session
