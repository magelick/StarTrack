import datetime
from typing import Optional

from pydantic import Field, PositiveInt

from src.database.enums import ChildPulseRecoveryStatusEnum
from src.schemas.base import DTO
from src.schemas.custom_types import AlphaStr


class ChildDataBasic(DTO):
    """
    Basic Child Data schema
    """

    feedback: Optional[AlphaStr] = Field(
        default=None,
        title="Feedback",
        description="Feedback current child data",
    )
    pulse_recovery_status: Optional[ChildPulseRecoveryStatusEnum] = Field(
        default=None,
        title="Pulse Recovery Status",
        description="Pulse Recovery Status current child data",
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
    entry_type: AlphaStr = Field(
        default=...,
        max_length=128,
        title="Entry Type",
        description="Entry Type current child data",
    )
    child_id: PositiveInt = Field(
        default=...,
        title="Child ID",
        description="Child ID current child data",
    )


class ChildDataAddForm(ChildDataBasic):
    """
    Child Data add schema
    """

    ...


class ChildDataUpdateForm(ChildDataBasic):
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
