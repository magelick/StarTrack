from typing import List, Tuple

from fastapi import APIRouter, HTTPException, Request, Path
from fastapi.responses import ORJSONResponse
from fastapi_cache.decorator import cache
from fastapi_sso import GoogleSSO
from pydantic import PositiveInt
from sqlalchemy.exc import NoResultFound
from starlette import status

from src.schemas.child import ChildDetail
from src.schemas.token import TokenData
from src.schemas.user import UserDetail, UserRegisterForm, UserUpdateForm
from src.services.user import UserService
from src.dependencies import UOWDep, google_sso
from src.utils import create_access_token, create_refresh_token
from src.logger import logger

router = APIRouter(
    prefix="/auth", tags=["Users"], default_response_class=ORJSONResponse
)


@router.get(path="/google/login", name="OAuth2 across Google")
async def google_login(google: GoogleSSO = google_sso):
    try:
        return await google.get_login_redirect()
    except Exception as e:
        logger.error(e)


@router.get(
    path="/google/callback",
    response_model=dict,
    name="OAuth2 Google Callback",
)
async def google_callback(
    request: Request, google: GoogleSSO = google_sso
) -> dict | None:
    try:
        login_user = await google.verify_and_process(request)
        return dict(login_user)
    except Exception as e:
        logger.error(e)
        return None


@router.post(
    path="/users",
    status_code=status.HTTP_201_CREATED,
    response_model=Tuple[UserDetail, TokenData],
    name="Add user into DB",
)
async def register_user(
    uow: UOWDep, register_data: UserRegisterForm
) -> Tuple[UserDetail, TokenData]:
    """
    Add new user into db
    :param register_data:
    :param uow:
    :return:
    """
    try:
        new_user = await UserService().add_user(
            uow=uow, register_form=register_data  # type: ignore
        )
        access_token = create_access_token(sub=str(new_user.id))
        refresh_token = create_refresh_token(sub=str(new_user.id))
        token_data = TokenData(
            access_token=access_token, refresh_token=refresh_token
        )
        return new_user, token_data
    except Exception as e:
        logger.error(e)
        return None


@router.get(
    path="/users",
    status_code=status.HTTP_200_OK,
    response_model=List[UserDetail],
    name="Get all users",
)
@cache(expire=60)
async def get_list_of_users(uow: UOWDep) -> List[UserDetail]:
    """
    Get list of users
    :param uow:
    :return:
    """
    try:
        users = await UserService().get_users(uow=uow)
        return users
    except Exception as e:
        logger.error(e)
        return None


@router.get(
    path="/users/{user_id}/",
    status_code=status.HTTP_200_OK,
    response_model=UserDetail,
    name="Get user by ID",
)
@cache(expire=60)
async def get_user_by_id(
    uow: UOWDep, user_id: PositiveInt = Path(default=..., ge=1)  # type: ignore
) -> UserDetail:
    """
    Get user by ID
    :param uow:
    :param user_id:
    :return:
    """
    try:
        user = await UserService().get_user(uow=uow, id=user_id)
        return user
    except (NoResultFound, Exception) as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )


@router.put(
    path="/users/{user_id}/",
    status_code=status.HTTP_200_OK,
    response_model=UserDetail,
    name="Update user by ID",
)
async def update_user_by_id(
    uow: UOWDep,
    update_form: UserUpdateForm,
    user_id: PositiveInt = Path(default=..., ge=1),  # type: ignore
) -> UserDetail:
    """
    Update user
    :param uow:
    :param update_form:
    :param user_id:
    :return:
    """
    try:
        update_user = await UserService().update_user(
            uow=uow, update_form=update_form, id=user_id
        )
        return update_user
    except (NoResultFound, Exception) as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )


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
    except (NoResultFound, Exception) as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )


@router.get(
    path="/users/{user_id}/children/",
    status_code=status.HTTP_200_OK,
    response_model=List[ChildDetail],
    name="Get children of user",
)
async def get_children_user(
    uow: UOWDep, user_id: PositiveInt = Path(default=...)  # type: ignore
) -> List[ChildDetail]:
    """
    Get children of authenticated user
    """
    try:
        children = await UserService().get_user_children(
            uow=uow, user_id=user_id
        )
        return children
    except (NoResultFound, Exception) as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"{e}"
        )
