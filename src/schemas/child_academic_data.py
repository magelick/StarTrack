import datetime
from typing import Optional

from pydantic import Field, PositiveInt

from src.database.enums import ChildTowardStudyEnum
from src.schemas.base import DTO
from src.schemas.custom_types import AlphaStr


class ChildAcademicDataBasix(DTO):
    """
    Basic Child Academic Data schema
    """

    academic_performance: Optional[float] = Field(
        default=None,
        title="Academic Performance",
        description="Academic Performance current child academic data",
    )
    academic_achievements: Optional[float] = Field(
        default=None,
        title="Academic Achievements",
        description="Academic Achievements current child academic data",
    )
    work_time: Optional[int] = Field(
        default=None,
        title="Work Time",
        description="Work Time current child academic data",
    )
    attitude_towards_study: Optional[ChildTowardStudyEnum] = Field(
        default=None,
        title="Attitude Towards Study",
        description="Attitude Towards Study current child academic data",
    )
    areas_of_difficulty: Optional[AlphaStr] = Field(
        default=None,
        max_length=256,
        title="Areas of Difficulty",
        description="Areas of Difficulty current child academic data",
    )
    additional_support_needs: Optional[bool] = Field(
        default=True,
        title="Additional Support Needs",
        description="Additional Support Needs current child academic data",
    )
    subject_interest: Optional[AlphaStr] = Field(
        default=None,
        max_length=256,
        title="Subject Interest",
        description="Subject Interest current child academic data",
    )
    child_id: PositiveInt = Field(
        default=...,
        title="Child ID",
        description="Child ID current child academic data",
    )


class ChildAcademicDataAddForm(ChildAcademicDataBasix):
    """
    Child Academic Data add schema
    """

    ...


class ChildAcademicDataUpdateForm(ChildAcademicDataBasix):
    """
    Child Academic Data update schema
    """

    ...


class ChildAcademicDataDetail(ChildAcademicDataBasix):
    """
    Child Academic Data detail schema
    """

    id: PositiveInt = Field(
        default=..., title="ID", description="ID current child academic data"
    )
    date: datetime.date = Field(
        default=...,
        title="Date",
        description="Date current child academic data",
    )
