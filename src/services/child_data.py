from typing import List

from src.unit_of_work import AbstractUnitOfWork
from src.schemas.child_data import (
    ChildDataDetail,
    ChildDataAddForm,
    ChildDataUpdateForm,
)
from src.utils import (
    get_pulse_recovery_status,
    calculate_adolescence_info,
    get_child,
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
        self, uow: AbstractUnitOfWork, child_add_form: ChildDataAddForm
    ) -> ChildDataDetail:
        """
        Add new child data
        :param uow:
        :param child_add_form:
        :return:
        """
        async with uow:
            child_basic_data_add_data = child_add_form.model_dump()

            pulse_recovery_status = await get_pulse_recovery_status(
                lying_pulse=child_basic_data_add_data.get("lying_pulse"),
                standing_pulse=child_basic_data_add_data.get("standing_pulse"),
            )

            child_info = {
                "feedback": child_basic_data_add_data.get("feedback"),
                "child_id": child_basic_data_add_data.get("child_id"),
                "pulse_recovery_status": pulse_recovery_status,
            }

            new_child_data = await uow.child_datas.add_one(data=child_info)

            child_from_data = await get_child(
                uow_children=uow.children,
                uow_session=uow._session,  # type: ignore
                child_id=child_basic_data_add_data.get("child_id"),
            )

            adolescence_info = await calculate_adolescence_info(
                sitting_height=child_basic_data_add_data.get("sitting_height"),
                standing_height=child_from_data.height,
                birth_date=child_from_data.date_of_birth,
                body_mass=child_from_data.weight,
                gender=child_from_data.gender,
            )

            if adolescence_info is not None:
                new_child_data.current_adolescence_age = adolescence_info.get(
                    "current_age"
                )
                new_child_data.start_adolescence_age = adolescence_info.get(
                    "start_age"
                )
                new_child_data.peek_adolescence_age = adolescence_info.get(
                    "peak_age"
                )
                new_child_data.end_adolescence_age = adolescence_info.get(
                    "end_age"
                )
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
        self,
        uow: AbstractUnitOfWork,
        child_update_form: ChildDataUpdateForm,
        **filter_by
    ) -> ChildDataDetail:
        """
        Update some child data
        :param uow:
        :param child_update_form:
        :return:
        """
        async with uow:
            child_basic_data_update_data = child_update_form.model_dump()
            pulse_recovery_status = await get_pulse_recovery_status(
                lying_pulse=child_basic_data_update_data.get("lying_pulse"),
                standing_pulse=child_basic_data_update_data.get(
                    "standing_pulse"
                ),
            )

            child_info = {
                "feedback": child_basic_data_update_data.get("feedback"),
                "child_id": child_basic_data_update_data.get("child_id"),
                "pulse_recovery_status": pulse_recovery_status,
            }

            update_child_data = await uow.child_datas.update_one(
                child_info, **filter_by
            )

            child_from_data = await get_child(
                uow_children=uow.children,
                uow_session=uow._session,  # type: ignore
                child_id=child_basic_data_update_data.get("child_id"),
            )

            adolescence_info = await calculate_adolescence_info(
                sitting_height=child_basic_data_update_data.get(
                    "sitting_height"
                ),
                standing_height=child_from_data.height,
                birth_date=child_from_data.date_of_birth,
                body_mass=child_from_data.weight,
                gender=child_from_data.gender,
            )

            if adolescence_info is not None:
                update_child_data.current_adolescence_age = (
                    adolescence_info.get("current_age")
                )
                update_child_data.start_adolescence_age = adolescence_info.get(
                    "start_age"
                )
                update_child_data.peek_adolescence_age = adolescence_info.get(
                    "peak_age"
                )
                update_child_data.end_adolescence_age = adolescence_info.get(
                    "end_age"
                )
            await uow.commit()

            return ChildDataDetail.model_validate(
                update_child_data, from_attributes=True
            )

    async def delete_child_data(
        self, uow: AbstractUnitOfWork, **filter_by
    ) -> None:
        """
        Delete some child data
        :param uow:
        :return:
        """
        async with uow:
            await uow.child_datas.delete_one(**filter_by)
            await uow.commit()
