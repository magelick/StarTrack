import datetime
from typing import Optional

from pydantic import Field, PositiveInt

from src.schemas.base import DTO
from src.schemas.custom_types import AlphaStr


class ChildPhysicalDataBasic(DTO):
    """
    Basic Child Physical Data schema
    """

    physical_type: Optional[AlphaStr] = Field(
        default=None,
        max_length=256,
        title="Physical Type",
        description="Physical Type current child physical data",
    )
    daily_activity_level: Optional[int] = Field(
        default=None,
        title="Daily Activity Level",
        description="Daily Activity Level current child physical data",
    )
    flexibility: Optional[AlphaStr] = Field(
        default=None,
        max_length=128,
        title="Flexibility",
        description="Flexibility current child physical data",
    )
    coordination: Optional[AlphaStr] = Field(
        default=None,
        max_length=128,
        title="Coordination",
        description="Coordination current child physical data",
    )
    injuries_and_chronic_pains: Optional[AlphaStr] = Field(
        default=None,
        max_length=256,
        title="Injuries and Chronic Pains",
        description="Injuries and Chronic Pains current child physical data",
    )
    sports_achievements: Optional[AlphaStr] = Field(
        default=None,
        max_length=256,
        title="Sports Achievements",
        description="Sports Achievements current child physical data",
    )
    interests: Optional[AlphaStr] = Field(
        default=None,
        max_length=256,
        title="Interests",
        description="Interests current child physical data",
    )
    child_id: PositiveInt = Field(
        default=...,
        title="Child ID",
        description="Child ID current child physical data",
    )


class ChildPhysicalDataAddForm(ChildPhysicalDataBasic):
    """
    Child Physical Data add schema
    """

    ...


class ChildPhysicalDataUpdateForm(ChildPhysicalDataBasic):
    """
    Child Physical Data update schema
    """

    ...


class ChildPhysicalDataDetail(ChildPhysicalDataBasic):
    """
    Child Physical Data detail schema
    """

    id: PositiveInt = Field(
        default=..., title="ID", description="ID current child physical data"
    )
    date: datetime.date = Field(
        default=...,
        title="Date",
        description="Date current child physical data",
    )
