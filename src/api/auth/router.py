from pathlib import Path
from typing import List, Tuple

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import ORJSONResponse
from fastapi_cache.decorator import cache
from fastapi_sso import GoogleSSO
from pydantic import PositiveInt
from sqlalchemy.exc import NoResultFound
from starlette import status

from src.schemas.token import TokenData
from src.schemas.user import UserDetail, UserRegisterForm
from src.services.user import UserService
from src.dependencies import UOWDep, google_sso
from src.utils import create_access_token, create_refresh_token

router = APIRouter(
    prefix="/auth", tags=["Users"], default_response_class=ORJSONResponse
)


@router.get(path="/google/login", name="OAuth2 across Google")
async def google_login(google: GoogleSSO = google_sso):
    return await google.get_login_redirect()


@router.get(
    path="/google/callback",
    response_model=Tuple[UserDetail, TokenData],
    name="OAuth2 Google Callback",
)
async def google_callback(
    request: Request, uow: UOWDep, google: GoogleSSO = google_sso
) -> Tuple[UserDetail, TokenData]:
    login_user = await google.verify_and_process(request)
    user = await UserService().get_user(uow=uow, email=login_user.email)
    if user is None:
        data = {
            "email": login_user.email,
            "first_name": login_user.first_name,
            "last_name": login_user.last_name,
            "role": "Parent",
        }
        new_user = await UserService().register_user(
            uow=uow, register_form=UserRegisterForm(**data)  # type: ignore
        )
        return new_user
    access_token = await create_access_token(sub=str(user.id))
    refresh_token = await create_refresh_token(sub=str(user.id))
    token_data = TokenData(
        access_token=access_token, refresh_token=refresh_token
    )
    return user, token_data


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
    path="/users/{user_id}/",
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
