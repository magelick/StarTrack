from typing import List

from src.unit_of_work import AbstractUnitOfWork
from src.schemas.child_development_data import (
    ChildDevelopmentDataDetail,
    ChildDevelopmentDataAddForm,
    ChildDevelopmentDataUpdateForm,
)


class ChildDevelopmentDataService:
    """
    Child Development Data service
    """

    async def get_child_development_datas(
        self, uow: AbstractUnitOfWork
    ) -> List[ChildDevelopmentDataDetail]:
        """
        Get all child development datas
        :param uow:
        :return:
        """
        async with uow:
            child_development_datas = (
                await uow.child_development_datas.get_all()
            )
            return [
                ChildDevelopmentDataDetail.model_validate(
                    child_development_data, from_attributes=True
                )
                for child_development_data in child_development_datas
            ]

    async def add_child_development_data(
        self, uow: AbstractUnitOfWork, child: ChildDevelopmentDataAddForm
    ) -> ChildDevelopmentDataDetail:
        """
        Add new child development data
        :param uow:
        :param child:
        :return:
        """
        async with uow:
            new_child_development_data = (
                await uow.child_development_datas.add_one(child.model_dump())
            )
            await uow.commit()
            return ChildDevelopmentDataDetail.model_validate(
                new_child_development_data, from_attributes=True
            )

    async def get_child_development_data(
        self, uow: AbstractUnitOfWork, **filter_by
    ) -> ChildDevelopmentDataDetail:
        """
        Get child development data by some filter
        :param uow:
        :return:
        """
        async with uow:
            child_development_data = await uow.child_development_datas.get_one(
                **filter_by
            )
            return ChildDevelopmentDataDetail.model_validate(
                child_development_data, from_attributes=True
            )

    async def update_child_development_data(
        self,
        uow: AbstractUnitOfWork,
        child: ChildDevelopmentDataUpdateForm,
        **filter_by
    ) -> ChildDevelopmentDataDetail:
        """
        Update some child development data
        :param uow:
        :param child:
        :return:
        """
        async with uow:
            update_child_development_data = (
                await uow.child_development_datas.update_one(
                    child.model_dump(), **filter_by
                )
            )
            await uow.commit()
            return ChildDevelopmentDataDetail.model_validate(
                update_child_development_data, from_attributes=True
            )

    async def delete_child_development_data(
        self, uow: AbstractUnitOfWork, **filter_by
    ):
        """
        Delete some child development data
        :param uow:
        :return:
        """
        async with uow:
            await uow.child_development_datas.delete_one(**filter_by)
            await uow.commit()
