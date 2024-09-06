import datetime
from typing import Optional

from pydantic import Field, PositiveInt

from src.database.enums import ChildEmotionalStateEnum
from src.schemas.base import DTO
from src.schemas.custom_types import AlphaStr


class ChildHealthDataBasic(DTO):
    """
    Basic Child Health Data schema
    """

    current_symptoms: Optional[AlphaStr] = Field(
        default=None,
        max_length=256,
        title="Current Symptoms",
        description="Academic Performance current child health data",
    )
    frequency_of_illnesses: Optional[AlphaStr] = Field(
        default=None,
        max_length=256,
        title="Frequency of Illnesses",
        description="Frequency of Illnesses current child health data",
    )
    doctor_visits: Optional[PositiveInt] = Field(
        default=None,
        title="Doctor Visits",
        description="Doctor Visits current child health data",
    )
    stress_anxiety_depression: Optional[AlphaStr] = Field(
        default=None,
        max_length=256,
        title="Stress Anxiety Depression",
        description="Stress Anxiety Depression current child health data",
    )
    emotional_state: Optional[ChildEmotionalStateEnum] = Field(
        default=None,
        title="Emotional State",
        description="Emotional State current child health data",
    )
    child_id: PositiveInt = Field(
        default=...,
        title="Child ID",
        description="Child ID current child health data",
    )


class ChildHealthDataAddForm(ChildHealthDataBasic):
    """
    Child Health Data add schema
    """

    ...


class ChildHealthDataUpdateForm(ChildHealthDataBasic):
    """
    Child Health Data update schema
    """

    ...


class ChildHealthDataDetail(ChildHealthDataBasic):
    """
    Child Health Data detail schema
    """

    id: PositiveInt = Field(
        default=..., title="ID", description="ID current child health data"
    )
    date: datetime.date = Field(
        default=..., title="Date", description="Date current child health data"
    )
