from typing import List, Tuple

from fastapi import HTTPException
from starlette import status

from src.schemas.token import TokenData
from src.unit_of_work import AbstractUnitOfWork
from src.schemas.user import (
    UserDetail,
    UserRegisterForm,
    UserLoginForm,
    UserUpdateForm,
)

from src.utils import (
    create_hash_password,
    verify_password,
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
            register_user.password = await create_hash_password(
                register_user.password
            )
            await uow.commit()
            await uow.refresh(instance=register_user)
            access_token = await create_access_token(sub=str(register_user.id))
            print(access_token)
            refresh_token = await create_refresh_token(
                sub=str(register_user.id)
            )
            return (
                UserDetail.model_validate(register_user, from_attributes=True),
                TokenData(
                    access_token=access_token, refresh_token=refresh_token
                ),
            )

    async def login_user(
        self, uow: AbstractUnitOfWork, login_form: UserLoginForm
    ) -> Tuple[UserDetail, TokenData]:
        """
        Login user
        :param login_form:
        :param uow:
        :return:
        """
        async with uow:
            login_user = await uow.users.get_one(email=login_form.email)

            if login_user is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found",
                )

            if not await verify_password(
                password=login_form.password, hash_password=login_user.password
            ):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Incorrect password",
                )

            new_access_token = await create_access_token(sub=login_user.id)
            new_refresh_token = await create_refresh_token(sub=login_user.id)
            print(new_refresh_token)

            return (
                UserDetail.model_validate(
                    obj=login_user, from_attributes=True
                ),
                TokenData(
                    access_token=new_access_token,
                    refresh_token=new_refresh_token,
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
        Update user
        :param uow:
        :param update_form:
        :return:
        """
        async with uow:
            user = await uow.users.get_one(**filter_by)
            return UserDetail.model_validate(user, from_attributes=True)

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
