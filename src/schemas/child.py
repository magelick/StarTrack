import datetime
from typing import Union, Optional

from pydantic import Field, PositiveInt

from src.schemas.base import DTO
from src.schemas.custom_types import AlphaStr
from src.database.enums import ChildGenderEnum


class ChildBasic(DTO):
    """
    Basic Child schema
    """

    first_name: AlphaStr = Field(
        default=...,
        max_length=128,
        title="First Name",
        description="First name current child",
    )
    last_name: AlphaStr = Field(
        default=...,
        max_length=128,
        title="Last Name",
        description="Last name current child",
    )
    date_of_birth: datetime.date = Field(
        default=...,
        title="Birthday",
        description="Birthday current child",
    )
    gender: ChildGenderEnum = Field(
        default=..., title="Gender", description="Gender current child"
    )
    photo_url: Optional[str] = Field(
        default=None,
        max_length=256,
        title="Photo",
        description="Photo current child",
    )
    illness_history: Optional[AlphaStr] = Field(
        default=None,
        max_length=256,
        title="Illness History",
        description="Illness History current child",
    )
    medical_diagnoses: Optional[AlphaStr] = Field(
        default=None,
        max_length=256,
        title="Medical Diagnoses",
        description="Medical Diagnoses current child",
    )
    age: Union[float, PositiveInt] = Field(
        default=1, title="Age", description="Age current child"
    )


class ChildAddForm(ChildBasic):
    """
    Child add schema
    """

    ...


class ChildUpdateForm(ChildBasic):
    """
    Child update schema
    """

    ...


class ChildDetail(ChildBasic):
    """
    Child detail schema
    """

    id: PositiveInt = Field(
        default=..., title="ID", description="ID current child"
    )
