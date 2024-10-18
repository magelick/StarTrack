import json
from pathlib import Path

from fastapi_sso import GoogleSSO
from starlette import status
from starlette.requests import Request

from typing import Annotated

from fastapi import Depends, HTTPException

from src.unit_of_work import AbstractUnitOfWork, UnitOfWork


async def get_current_user(uow: AbstractUnitOfWork, request: Request):
    """
    Get current user
    :param uow:
    :param request:
    :return:
    """
    async with uow:
        user = await uow.users.get_one(id=request.user.identity)
        if not user:
            pass


def _is_authenticated(request: Request):
    """

    :param request:
    :return:
    """
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
UOWDep = Annotated[AbstractUnitOfWork, Depends(dependency=UnitOfWork)]
is_authenticated = Depends(dependency=_is_authenticated)
google_sso = Depends(dependency=get_google_sso)
