from typing import List

from src.unit_of_work import AbstractUnitOfWork
from src.schemas.user import UserDetail


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
