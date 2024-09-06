from typing import List

from src.unit_of_work import AbstractUnitOfWork
from src.schemas.child_data import (
    ChildDataDetail,
    ChildDataAddForm,
    ChildDataUpdateForm,
)


class ChildDataService:
    """
    Child Data service
    """

    async def get_child_datas(
        self, uow: AbstractUnitOfWork
    ) -> List[ChildDataDetail]:
        """
        Get all child datas
        :param uow:
        :return:
        """
        async with uow:
            child_datas = await uow.child_datas.get_all()
            return [
                ChildDataDetail.model_validate(
                    child_data, from_attributes=True
                )
                for child_data in child_datas
            ]

    async def add_child_data(
        self, uow: AbstractUnitOfWork, child: ChildDataAddForm
    ) -> ChildDataDetail:
        """
        Add new child data
        :param uow:
        :param child:
        :return:
        """
        async with uow:
            new_child_data = await uow.child_datas.add_one(child.model_dump())
            await uow.commit()
            return ChildDataDetail.model_validate(
                new_child_data, from_attributes=True
            )

    async def get_child_data(
        self, uow: AbstractUnitOfWork, **filter_by
    ) -> ChildDataDetail:
        """
        Get child data by some filter
        :param uow:
        :return:
        """
        async with uow:
            child_data = await uow.child_datas.get_one(**filter_by)
            return ChildDataDetail.model_validate(
                child_data, from_attributes=True
            )

    async def update_child_data(
        self, uow: AbstractUnitOfWork, child: ChildDataUpdateForm, **filter_by
    ) -> ChildDataDetail:
        """
        Update some child data
        :param uow:
        :param child:
        :return:
        """
        async with uow:
            update_child_data = await uow.child_datas.update_one(
                child.model_dump(), **filter_by
            )
            await uow.commit()
            return ChildDataDetail.model_validate(
                update_child_data, from_attributes=True
            )

    async def delete_child_data(self, uow: AbstractUnitOfWork, **filter_by):
        """
        Delete some child data
        :param uow:
        :return:
        """
        async with uow:
            await uow.child_datas.delete_one(**filter_by)
            await uow.commit()
