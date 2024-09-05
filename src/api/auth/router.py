from pathlib import Path
from typing import List, Tuple

from fastapi import APIRouter, HTTPException
from fastapi.responses import ORJSONResponse
from fastapi_cache.decorator import cache
from pydantic import PositiveInt
from sqlalchemy.exc import NoResultFound
from starlette import status

from src.schemas.token import TokenData
from src.schemas.user import UserRegisterForm, UserDetail, UserLoginForm
from src.services.user import UserService
from src.dependencies import UOWDep

router = APIRouter(
    prefix="/auth", tags=["Users"], default_response_class=ORJSONResponse
)


@router.post(
    path="/register",
    status_code=status.HTTP_201_CREATED,
    response_model=Tuple[UserDetail, TokenData],
    response_model_exclude={"password"},
    name="Register user",
)
async def register_user(
    uow: UOWDep, register_form: UserRegisterForm
) -> Tuple[UserDetail, TokenData]:
    """
    Register user
    :param uow:
    :param register_form:
    :return:
    """
    new_user = await UserService().register_user(
        uow=uow, register_form=register_form
    )
    return new_user


@router.post(
    path="/login",
    status_code=status.HTTP_201_CREATED,
    response_model=Tuple[UserDetail, TokenData],
    name="Login user",
)
async def login_user(
    uow: UOWDep, login_form: UserLoginForm
) -> Tuple[UserDetail, TokenData]:
    """
    Login user
    :param uow:
    :param login_form:
    :return:
    """
    login = await UserService().login_user(uow=uow, login_form=login_form)
    return login


@router.post(
    path="/token/{refresh_token}",
    status_code=status.HTTP_200_OK,
    response_model=TokenData,
    name="Refresh access token",
)
@cache(expire=120)
async def refresh_access_token(refresh_token: str) -> TokenData:
    """
    Refresh access token
    :param refresh_token:
    :return:
    """
    tokens = await UserService().refresh_access_token(
        refresh_token=refresh_token
    )
    return tokens


@router.get(
    path="/users",
    status_code=status.HTTP_200_OK,
    response_model=List[UserDetail],
    name="Get all users",
)
@cache(expire=120)
async def get_list_of_users(uow: UOWDep) -> List[UserDetail]:
    """
    Get list of users
    :param uow:
    :return:
    """
    users = await UserService().get_users(uow=uow)
    return users


@router.delete(
    path="/{user_id}/",
    status_code=status.HTTP_200_OK,
    name="Delete user by ID",
)
async def delete_user_by_id(
    uow: UOWDep, user_id: PositiveInt = Path(default=..., ge=1)  # type: ignore
):
    """
    Delete user by ID
    :param uow:
    :param user_id:
    :return:
    """
    try:
        await UserService().delete_user(uow=uow, id=user_id)
        return {"msg": "User has been successfully removed"}
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
