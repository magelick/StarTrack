from typing import List

from src.unit_of_work import AbstractUnitOfWork
from src.schemas.child_medical_data import (
    ChildMedicalDataDetail,
    ChildMedicalDataAddForm,
    ChildMedicalDataUpdateForm,
)


class ChildMedicalDataService:
    """
    Child Medical Data service
    """

    async def get_child_medical_datas(
        self, uow: AbstractUnitOfWork
    ) -> List[ChildMedicalDataDetail]:
        """
        Get all child medical data
        :param uow:
        :return:
        """
        async with uow:
            child_medical_datas = await uow.child_medical_datas.get_all()
            return [
                ChildMedicalDataDetail.model_validate(
                    child_medical_data, from_attributes=True
                )
                for child_medical_data in child_medical_datas
            ]

    async def add_child_medical_data(
        self, uow: AbstractUnitOfWork, child: ChildMedicalDataAddForm
    ) -> ChildMedicalDataDetail:
        """
        Add new child medical data
        :param uow:
        :param child:
        :return:
        """
        async with uow:
            new_child_medical_data = await uow.child_medical_datas.add_one(
                child.model_dump()
            )
            await uow.commit()
            return ChildMedicalDataDetail.model_validate(
                new_child_medical_data, from_attributes=True
            )

    async def get_child_medical_data(
        self, uow: AbstractUnitOfWork, **filter_by
    ) -> ChildMedicalDataDetail:
        """
        Get child medical data by some filter
        :param uow:
        :return:
        """
        async with uow:
            child_medical_data = await uow.child_medical_datas.get_one(
                **filter_by
            )
            return ChildMedicalDataDetail.model_validate(
                child_medical_data, from_attributes=True
            )

    async def update_child_medical_data(
        self,
        uow: AbstractUnitOfWork,
        child: ChildMedicalDataUpdateForm,
        **filter_by
    ) -> ChildMedicalDataDetail:
        """
        Update some child medical data
        :param uow:
        :param child:
        :return:
        """
        async with uow:
            update_child_medical_data = (
                await uow.child_medical_datas.update_one(
                    child.model_dump(), **filter_by
                )
            )
            await uow.commit()
            return ChildMedicalDataDetail.model_validate(
                update_child_medical_data, from_attributes=True
            )

    async def delete_child_medical_data(
        self, uow: AbstractUnitOfWork, **filter_by
    ):
        """
        Delete some child medical data
        :param uow:
        :return:
        """
        async with uow:
            await uow.child_medical_datas.delete_one(**filter_by)
            await uow.commit()
