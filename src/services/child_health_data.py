from typing import List

from src.unit_of_work import AbstractUnitOfWork
from src.schemas.child_health_data import (
    ChildHealthDataDetail,
    ChildHealthDataAddForm,
    ChildHealthDataUpdateForm,
)


class ChildHealthDataService:
    """
    Child Health Data service
    """

    async def get_child_health_datas(
        self, uow: AbstractUnitOfWork
    ) -> List[ChildHealthDataDetail]:
        """
        Get all child health datas
        :param uow:
        :return:
        """
        async with uow:
            child_health_datas = await uow.child_health_datas.get_all()
            return [
                ChildHealthDataDetail.model_validate(
                    child_health_data, from_attributes=True
                )
                for child_health_data in child_health_datas
            ]

    async def add_child_health_data(
        self, uow: AbstractUnitOfWork, child: ChildHealthDataAddForm
    ) -> ChildHealthDataDetail:
        """
        Add new child health data
        :param uow:
        :param child:
        :return:
        """
        async with uow:
            new_child_health_data = await uow.child_health_datas.add_one(
                child.model_dump()
            )
            await uow.commit()
            return ChildHealthDataDetail.model_validate(
                new_child_health_data, from_attributes=True
            )

    async def get_child_health_data(
        self, uow: AbstractUnitOfWork, **filter_by
    ) -> ChildHealthDataDetail:
        """
        Get child health data by some filter
        :param uow:
        :return:
        """
        async with uow:
            child_health_data = await uow.child_health_datas.get_one(
                **filter_by
            )
            return ChildHealthDataDetail.model_validate(
                child_health_data, from_attributes=True
            )

    async def update_child_data(
        self,
        uow: AbstractUnitOfWork,
        child: ChildHealthDataUpdateForm,
        **filter_by
    ) -> ChildHealthDataDetail:
        """
        Update some child health data
        :param uow:
        :param child:
        :return:
        """
        async with uow:
            update_child_health_data = await uow.child_health_datas.update_one(
                child.model_dump(), **filter_by
            )
            await uow.commit()
            return ChildHealthDataDetail.model_validate(
                update_child_health_data, from_attributes=True
            )

    async def delete_child_health_data(
        self, uow: AbstractUnitOfWork, **filter_by
    ):
        """
        Delete some child health data
        :param uow:
        :return:
        """
        async with uow:
            await uow.child_health_datas.delete_one(**filter_by)
            await uow.commit()
