import json
from pathlib import Path
from typing import AsyncGenerator

from fastapi_sso import GoogleSSO
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


def load_google_secrets() -> dict:
    """
    Dependency which load google secret for client_secrets.json
    :return:
    """
    path_to_secrets = Path("client_secrets.json")

    with path_to_secrets.open("r") as file:
        secrets = json.load(file)

    web_secrets = secrets.get("web", {})

    if not web_secrets:
        raise ValueError("Некорректный формат файла client_secrets.json")

    return {
        "client_id": web_secrets["client_id"],
        "client_secret": web_secrets["client_secret"],
        "redirect_uri": web_secrets["redirect_uris"][0],
    }


def get_google_sso() -> GoogleSSO:
    """
    Dependency which return GoogleSSO instance
    :return:
    """
    google_secrets = load_google_secrets()

    return GoogleSSO(
        client_id=google_secrets["client_id"],
        client_secret=google_secrets["client_secret"],
        redirect_uri=google_secrets["redirect_uri"],
    )


# Initial FastAPI dependencies
get_async_db_session = Annotated[
    AsyncGenerator[AsyncSession, None], Depends(dependency=_get_async_session)
]
UOWDep = Annotated[AbstractUnitOfWork, Depends(dependency=UnitOfWork)]
is_authenticated = Depends(dependency=_is_authenticated)
google_sso = Depends(dependency=get_google_sso)
