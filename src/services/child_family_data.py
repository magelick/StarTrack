from typing import List

from src.unit_of_work import AbstractUnitOfWork
from src.schemas.child_family_data import (
    ChildFamilyDataDetail,
    ChildFamilyDataAddForm,
    ChildFamilyDataUpdateForm,
)


class ChildFamilyDataService:
    """
    Child Family Data service
    """

    async def get_child_family_datas(
        self, uow: AbstractUnitOfWork
    ) -> List[ChildFamilyDataDetail]:
        """
        Get all child family datas
        :param uow:
        :return:
        """
        async with uow:
            child_family_datas = await uow.child_family_datas.get_all()
            return [
                ChildFamilyDataDetail.model_validate(
                    child_family_data, from_attributes=True
                )
                for child_family_data in child_family_datas
            ]

    async def add_child_family_data(
        self, uow: AbstractUnitOfWork, child: ChildFamilyDataAddForm
    ) -> ChildFamilyDataDetail:
        """
        Add new child family data
        :param uow:
        :param child:
        :return:
        """
        async with uow:
            new_child_family_data = await uow.child_family_datas.add_one(
                child.model_dump()
            )
            await uow.commit()
            return ChildFamilyDataDetail.model_validate(
                new_child_family_data, from_attributes=True
            )

    async def get_child_family_data(
        self, uow: AbstractUnitOfWork, **filter_by
    ) -> ChildFamilyDataDetail:
        """
        Get child family data by some filter
        :param uow:
        :return:
        """
        async with uow:
            child_family_data = await uow.child_family_datas.get_one(
                **filter_by
            )
            return ChildFamilyDataDetail.model_validate(
                child_family_data, from_attributes=True
            )

    async def update_child_family_data(
        self,
        uow: AbstractUnitOfWork,
        child: ChildFamilyDataUpdateForm,
        **filter_by
    ) -> ChildFamilyDataDetail:
        """
        Update some child family data
        :param uow:
        :param child:
        :return:
        """
        async with uow:
            update_child_family_data = await uow.child_family_datas.update_one(
                child.model_dump(), **filter_by
            )
            await uow.commit()
            return ChildFamilyDataDetail.model_validate(
                update_child_family_data, from_attributes=True
            )

    async def delete_child_family_data(
        self, uow: AbstractUnitOfWork, **filter_by
    ):
        """
        Delete some child family data
        :param uow:
        :return:
        """
        async with uow:
            await uow.child_family_datas.delete_one(**filter_by)
            await uow.commit()
