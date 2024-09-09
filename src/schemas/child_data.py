import datetime
from typing import Optional

from pydantic import Field, PositiveInt

from src.database.enums import ChildPulseRecoveryStatusEnum
from src.schemas.base import DTO


class ChildDataBasic(DTO):
    """
    Basic Child Data schema
    """

    feedback: Optional[str] = Field(
        default=None,
        title="Feedback",
        description="Feedback current child data",
    )
    child_id: PositiveInt = Field(
        default=...,
        title="Child ID",
        description="Child ID current child data",
    )


class ChildDataForm(ChildDataBasic):
    """
    Child Data schema for forms
    """

    lying_pulse: int = Field(
        default=...,
        title="Lying Pulse",
        description="Lying Pulse current child data",
    )
    standing_pulse: int = Field(
        default=...,
        title="Lying Pulse",
        description="Lying Pulse current child data",
    )
    sitting_height: Optional[float] = Field(
        default=None,
        title="Sitting Height",
        description="Sitting Height current child data",
    )


class ChildDataAddForm(ChildDataForm):
    """
    Child Data add schema
    """

    ...


class ChildDataUpdateForm(ChildDataForm):
    """
    Child Data update schema
    """

    ...


class ChildDataDetail(ChildDataBasic):
    """
    Child Data detail schema
    """

    id: PositiveInt = Field(
        default=..., title="ID", description="ID current child data"
    )
    date: datetime.date = Field(
        default=..., title="Date", description="Date current child data"
    )
    pulse_recovery_status: Optional[ChildPulseRecoveryStatusEnum] = Field(
        default=None,
        title="Pulse Recovery Status",
        description="Pulse Recovery Status current child data",
    )
    current_adolescence_age: float = Field(
        default=...,
        title="Start adolescence age",
        description="Start adolescence age current child data",
    )
    start_adolescence_age: float = Field(
        default=...,
        title="Start adolescence age",
        description="Start adolescence age current child data",
    )
    peek_adolescence_age: float = Field(
        default=...,
        title="Peek adolescence age",
        description="Peek adolescence age current child data",
    )
    end_adolescence_age: float = Field(
        default=...,
        title="End adolescence age",
        description="End adolescence age current child data",
    )
