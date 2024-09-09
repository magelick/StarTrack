from typing import List

from src.unit_of_work import AbstractUnitOfWork
from src.schemas.child_academic_data import (
    ChildAcademicDataDetail,
    ChildAcademicDataAddForm,
    ChildAcademicDataUpdateForm,
)
from src.utils import calculate_subject_gpa, calculate_progress_ratio


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
            child_academic_add_data = child.model_dump()

            child_academic_info = {
                "academic_performance": child_academic_add_data.get(
                    "academic_performance"
                ),
                "academic_achievements": child_academic_add_data.get(
                    "academic_achievements"
                ),
                "work_time": child_academic_add_data.get("work_time"),
                "attitude_towards_study": child_academic_add_data.get(
                    "attitude_towards_study"
                ),
                "areas_of_difficulty": child_academic_add_data.get(
                    "areas_of_difficulty"
                ),
                "additional_support_needs": child_academic_add_data.get(
                    "additional_support_needs"
                ),
                "subject_interest": child_academic_add_data.get(
                    "subject_interest"
                ),
                "child_id": child_academic_add_data.get("child_id"),
            }

            new_child_academic_data = await uow.child_academic_datas.add_one(
                child_academic_info
            )
            new_child_academic_data.subject_gpa = await calculate_subject_gpa(
                grades=child_academic_add_data.get("grades")
            )
            new_child_academic_data.progress_ratio = (
                await calculate_progress_ratio(
                    current_avg_grade=child_academic_add_data.get(
                        "current_avg_grade"
                    ),
                    previous_avg_grade=child_academic_add_data.get(
                        "previous_avg_grade"
                    ),
                )
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
            child_academic_update_data = child.model_dump()

            child_academic_info = {
                "academic_performance": child_academic_update_data.get(
                    "academic_performance"
                ),
                "academic_achievements": child_academic_update_data.get(
                    "academic_achievements"
                ),
                "work_time": child_academic_update_data.get("work_time"),
                "attitude_towards_study": child_academic_update_data.get(
                    "attitude_towards_study"
                ),
                "areas_of_difficulty": child_academic_update_data.get(
                    "areas_of_difficulty"
                ),
                "additional_support_needs": child_academic_update_data.get(
                    "additional_support_needs"
                ),
                "subject_interest": child_academic_update_data.get(
                    "subject_interest"
                ),
                "child_id": child_academic_update_data.get("child_id"),
            }

            update_child_academic_data = (
                await uow.child_academic_datas.update_one(
                    child_academic_info, **filter_by
                )
            )
            update_child_academic_data.subject_gpa = (
                await calculate_subject_gpa(
                    grades=child_academic_update_data.get("grades")
                )
            )
            update_child_academic_data.progress_ratio = (
                await calculate_progress_ratio(
                    current_avg_grade=child_academic_update_data.get(
                        "current_avg_grade"
                    ),
                    previous_avg_grade=child_academic_update_data.get(
                        "previous_avg_grade"
                    ),
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
