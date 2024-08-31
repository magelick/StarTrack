import datetime
import enum
from typing import Union

from pydantic import Field, PositiveInt

from src.schemas.base import DTO
from src.schemas.custom_types import AlphaStr


class ChildBasic(DTO):
    """
    Basic Child schema
    """

    first_name: AlphaStr = Field(
        default=...,
        max_length=100,
        title="Child First Name",
        description="First name current child",
    )
    last_name: AlphaStr = Field(
        default=...,
        max_length=100,
        title="Child Last Name",
        description="Last name current child",
    )
    date_of_birth: datetime.date = Field(
        default=...,
        title="Child Birthday",
        description="Birthday current child",
    )
    gender: enum.Enum = Field(
        default=..., title="Child Gender", description="Gender current child"
    )
    photo_url: str = Field(
        default=...,
        max_length=200,
        title="Child Photo",
        description="Photo current child",
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
        default=..., title="Child ID", description="ID current child"
    )
    age: Union[float, PositiveInt] = Field(
        default=..., title="Child Age", description="Age current child"
    )
