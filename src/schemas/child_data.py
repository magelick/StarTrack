import datetime
from typing import Optional

from pydantic import Field, PositiveInt

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
    pulse_recovery_status: Optional[AlphaStr] = Field(
        default=None,
        max_length=128,
        title="Pulse Recovery Status",
        description="Pulse Recovery Status current child data",
    )
    adolescence_info: Optional[AlphaStr] = Field(
        default=None,
        max_length=256,
        title="Adolescence Info",
        description="Adolescence Info current child data",
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
