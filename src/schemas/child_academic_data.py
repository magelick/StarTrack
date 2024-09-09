import datetime
from typing import Optional

from pydantic import Field, PositiveInt

from src.database.enums import ChildTowardStudyEnum
from src.schemas.base import DTO


class ChildAcademicDataBasic(DTO):
    """
    Basic Child Academic Data schema
    """

    academic_performance: Optional[float] = Field(
        default=None,
        title="Academic Performance",
        description="Academic Performance current child academic data",
    )
    academic_achievements: Optional[str] = Field(
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
    areas_of_difficulty: Optional[str] = Field(
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
    subject_interest: Optional[str] = Field(
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


class ChildAcademicDataForm(ChildAcademicDataBasic):
    """
    Basic Child Academic Data form schema
    """

    grades: Optional[list[int]] = Field(
        default=None,
        title="Grades",
        description="Grades current child academic data",
    )
    current_avg_grade: Optional[int] = Field(
        default=None,
        title="Current AVG grade",
        description="Current AVG grade current child academic data",
    )
    previous_avg_grade: Optional[int] = Field(
        default=None,
        title="Previous AVG grade",
        description="Previous AVG grade current child academic data",
    )


class ChildAcademicDataAddForm(ChildAcademicDataForm):
    """
    Child Academic Data add schema
    """

    ...


class ChildAcademicDataUpdateForm(ChildAcademicDataForm):
    """
    Child Academic Data update schema
    """

    ...


class ChildAcademicDataDetail(ChildAcademicDataBasic):
    """
    Child Academic Data detail schema
    """

    id: PositiveInt = Field(
        default=..., title="ID", description="ID current child academic data"
    )
    subject_gpa: Optional[float] = Field(
        default=None,
        title="Subject GPA",
        description="Subject GPA current child academic data",
    )
    progress_ratio: Optional[float] = Field(
        default=None,
        title="Progress Ratio",
        description="Progress Ratio current academic data",
    )
    date: datetime.date = Field(
        default=...,
        title="Date",
        description="Date current child academic data",
    )
