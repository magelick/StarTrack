from typing import List, Tuple

from fastapi import HTTPException
from sqlalchemy.exc import NoResultFound
from starlette import status

from src.schemas.token import TokenData
from src.unit_of_work import AbstractUnitOfWork
from src.schemas.user import (
    UserDetail,
    UserRegisterForm,
    UserUpdateForm,
)

from src.utils import (
    create_access_token,
    create_refresh_token,
    verify_refresh_token,
)


class UserService:
    """
    User service
    """

    async def get_users(self, uow: AbstractUnitOfWork) -> List[UserDetail]:
        """
        Get all users
        :param uow:
        :return:
        """
        async with uow:
            users = await uow.users.get_all()
            return [
                UserDetail.model_validate(user, from_attributes=True)
                for user in users
            ]

    async def register_user(
        self, uow: AbstractUnitOfWork, register_form: UserRegisterForm
    ) -> Tuple[UserDetail, TokenData]:
        """
        Register user
        :param register_form:
        :param uow:
        :return:
        """
        async with uow:
            register_user = await uow.users.add_one(register_form.model_dump())
            await uow.commit()
            access_token = await create_access_token(sub=str(register_user.id))
            refresh_token = await create_refresh_token(
                sub=str(register_user.id)
            )
            return (
                UserDetail.model_validate(register_user, from_attributes=True),
                TokenData(
                    access_token=access_token, refresh_token=refresh_token
                ),
            )

    async def refresh_access_token(self, refresh_token: str) -> TokenData:
        """
        Create new access token by refresh token
        :return:
        """
        user_id = await verify_refresh_token(refresh_token=refresh_token)

        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token = await create_access_token(sub=str(user_id.get("sub")))

        return TokenData(
            access_token=access_token, refresh_token=refresh_token
        )

    async def get_user(
        self, uow: AbstractUnitOfWork, **filter_by
    ) -> UserDetail:
        """
        Get user
        :param uow:
        :param update_form:
        :return:
        """
        async with uow:
            try:
                user = await uow.users.get_one(**filter_by)
                return UserDetail.model_validate(user, from_attributes=True)
            except NoResultFound:
                return None

    async def update_user(
        self, uow: AbstractUnitOfWork, update_form: UserUpdateForm, **filter_by
    ) -> UserDetail:
        """
        Update user
        :param uow:
        :param update_form:
        :return:
        """
        async with uow:
            update_user = await uow.users.update_one(
                update_form.model_dump(), **filter_by
            )
            await uow.commit()
            return UserDetail.model_validate(update_user, from_attributes=True)

    async def delete_user(self, uow: AbstractUnitOfWork, **filter_by):
        """
        Delete user
        :param uow:
        :param filter_by:
        :return:
        """
        async with uow:
            await uow.users.delete_one(**filter_by)
            await uow.commit()
