from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.requests import Request

from src.database.models import Base

from typing import Annotated

from fastapi import Depends, HTTPException, WebSocket

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


class ConnectionManager:
    """
    # Class for saving client active session
    """

    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


# Initial FastAPI dependencies
get_async_db_session = Annotated[
    AsyncGenerator[AsyncSession, None], Depends(dependency=_get_async_session)
]
UOWDep = Annotated[AbstractUnitOfWork, Depends(dependency=UnitOfWork)]
is_authenticated = Depends(dependency=_is_authenticated)
ChatSession = Depends(dependency=ConnectionManager)
