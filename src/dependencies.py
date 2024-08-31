from src.database.models import Base


async def get_async_session():
    """
    Depend,which create session to database
    :return:
    """
    async with Base.async_session_maker() as session:
        yield session
