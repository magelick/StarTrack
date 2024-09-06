from typing import List

from src.unit_of_work import AbstractUnitOfWork
from src.schemas.child_physical_data import (
    ChildPhysicalDataDetail,
    ChildPhysicalDataAddForm,
    ChildPhysicalDataUpdateForm,
)


class ChildPhysicalDataService:
    """
    Child Physical Data service
    """

    async def get_child_physical_datas(
        self, uow: AbstractUnitOfWork
    ) -> List[ChildPhysicalDataDetail]:
        """
        Get all child physical datas
        :param uow:
        :return:
        """
        async with uow:
            child_physical_datas = await uow.child_physical_datas.get_all()
            return [
                ChildPhysicalDataDetail.model_validate(
                    child_physical_data, from_attributes=True
                )
                for child_physical_data in child_physical_datas
            ]

    async def add_child_physical_data(
        self, uow: AbstractUnitOfWork, child: ChildPhysicalDataAddForm
    ) -> ChildPhysicalDataDetail:
        """
        Add new child physical data
        :param uow:
        :param child:
        :return:
        """
        async with uow:
            new_child_physical_data = await uow.child_physical_datas.add_one(
                child.model_dump()
            )
            await uow.commit()
            return ChildPhysicalDataDetail.model_validate(
                new_child_physical_data, from_attributes=True
            )

    async def get_child_physical_data(
        self, uow: AbstractUnitOfWork, **filter_by
    ) -> ChildPhysicalDataDetail:
        """
        Get child physical data by some filter
        :param uow:
        :return:
        """
        async with uow:
            child_physical_data = await uow.child_physical_datas.get_one(
                **filter_by
            )
            return ChildPhysicalDataDetail.model_validate(
                child_physical_data, from_attributes=True
            )

    async def update_child_physical_data(
        self,
        uow: AbstractUnitOfWork,
        child: ChildPhysicalDataUpdateForm,
        **filter_by
    ) -> ChildPhysicalDataDetail:
        """
        Update some child physical data
        :param uow:
        :param child:
        :return:
        """
        async with uow:
            update_child_physical_data = (
                await uow.child_physical_datas.update_one(
                    child.model_dump(), **filter_by
                )
            )
            await uow.commit()
            return ChildPhysicalDataDetail.model_validate(
                update_child_physical_data, from_attributes=True
            )

    async def delete_child_physical_data(
        self, uow: AbstractUnitOfWork, **filter_by
    ):
        """
        Delete some child physical data
        :param uow:
        :return:
        """
        async with uow:
            await uow.child_physical_datas.delete_one(**filter_by)
            await uow.commit()
