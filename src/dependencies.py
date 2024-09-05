from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.requests import Request

from src.database.models import Base

from typing import Annotated

from fastapi import Depends, HTTPException

from src.unit_of_work import AbstractUnitOfWork, UnitOfWork


async def _get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Depend,which create session to database
    :return:
    """
    async with Base.async_session_maker() as session:
        yield session


def _is_authenticated(request: Request):
    if not request.user.is_authenticated:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User is not authorization",
        )


# Initial FastAPI dependencies
get_async_db_session = Annotated[
    AsyncGenerator[AsyncSession, None], Depends(_get_async_session)
]
UOWDep = Annotated[AbstractUnitOfWork, Depends(UnitOfWork)]
is_authenticated = Depends(dependency=_is_authenticated)
