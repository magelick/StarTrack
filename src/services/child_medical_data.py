from typing import List

from src.unit_of_work import AbstractUnitOfWork
from src.schemas.child_medical_data import (
    ChildMedicalDataDetail,
    ChildMedicalDataAddForm,
    ChildMedicalDataUpdateForm,
)
from src.utils import calculate_bsa, get_child, calculate_rohrer_index


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
            child_medical_data_add_data = child.model_dump()

            child_from_data = await get_child(
                uow_children=uow.children,
                uow_session=uow._session,  # type: ignore
                child_id=child_medical_data_add_data.get("child_id"),
            )
            new_child_medical_data = await uow.child_medical_datas.add_one(
                child_medical_data_add_data
            )
            new_child_medical_data.bsa_index = await calculate_bsa(
                height_cm=child_from_data.height,
                weight_kg=child_from_data.weight,
            )
            rohrer_index, _ = await calculate_rohrer_index(
                height_cm=child_from_data.height,
                weight_kg=child_from_data.weight,
            )
            new_child_medical_data.rohrer_index = rohrer_index
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
            child_medical_data_update_data = child.model_dump()

            child_from_data = await get_child(
                uow_children=uow.children,
                uow_session=uow._session,  # type: ignore
                child_id=child_medical_data_update_data.get("child_id"),
            )

            update_child_medical_data = (
                await uow.child_medical_datas.update_one(
                    child.model_dump(), **filter_by
                )
            )
            update_child_medical_data.bsa_index = await calculate_bsa(
                height_cm=child_from_data.height,
                weight_kg=child_from_data.weight,
            )
            rohrer_index, _ = await calculate_rohrer_index(
                height_cm=child_from_data.height,
                weight_kg=child_from_data.weight,
            )
            update_child_medical_data.rohrer_index = rohrer_index
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
