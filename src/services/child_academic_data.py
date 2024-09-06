from typing import List

from src.unit_of_work import AbstractUnitOfWork
from src.schemas.child_academic_data import (
    ChildAcademicDataDetail,
    ChildAcademicDataAddForm,
    ChildAcademicDataUpdateForm,
)


class ChildAcademicDataService:
    """
    Child Academic Data service
    """

    async def get_child_academic_datas(
        self, uow: AbstractUnitOfWork
    ) -> List[ChildAcademicDataDetail]:
        """
        Get all child academic datas
        :param uow:
        :return:
        """
        async with uow:
            child_academic_datas = await uow.child_academic_datas.get_all()
            return [
                ChildAcademicDataDetail.model_validate(
                    child_academic_data, from_attributes=True
                )
                for child_academic_data in child_academic_datas
            ]

    async def add_child_academic_data(
        self, uow: AbstractUnitOfWork, child: ChildAcademicDataAddForm
    ) -> ChildAcademicDataDetail:
        """
        Add new child academic data
        :param uow:
        :param child:
        :return:
        """
        async with uow:
            new_child_academic_data = await uow.child_academic_datas.add_one(
                child.model_dump()
            )
            await uow.commit()
            return ChildAcademicDataDetail.model_validate(
                new_child_academic_data, from_attributes=True
            )

    async def get_child_academic_data(
        self, uow: AbstractUnitOfWork, **filter_by
    ) -> ChildAcademicDataDetail:
        """
        Get child academic data by some filter
        :param uow:
        :return:
        """
        async with uow:
            child_academic_data = await uow.child_academic_datas.get_one(
                **filter_by
            )
            return ChildAcademicDataDetail.model_validate(
                child_academic_data, from_attributes=True
            )

    async def update_child_academic_data(
        self,
        uow: AbstractUnitOfWork,
        child: ChildAcademicDataUpdateForm,
        **filter_by
    ) -> ChildAcademicDataDetail:
        """
        Update some child academic data
        :param uow:
        :param child:
        :return:
        """
        async with uow:
            update_child_academic_data = (
                await uow.child_academic_datas.update_one(
                    child.model_dump(), **filter_by
                )
            )
            await uow.commit()
            return ChildAcademicDataDetail.model_validate(
                update_child_academic_data, from_attributes=True
            )

    async def delete_child_academic_data(
        self, uow: AbstractUnitOfWork, **filter_by
    ):
        """
        Delete some child academic data
        :param uow:
        :return:
        """
        async with uow:
            await uow.child_academic_datas.delete_one(**filter_by)
            await uow.commit()
