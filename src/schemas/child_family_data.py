import datetime
from typing import Optional

from pydantic import Field, PositiveInt

from src.database.enums import (
    ChildParentingMethodsEnum,
    ChildParentalAttentionEnum,
)
from src.schemas.base import DTO
from src.schemas.custom_types import AlphaStr


class ChildFamilyDataBasic(DTO):
    """
    Basic Child Family Data schema
    """

    family_info: Optional[AlphaStr] = Field(
        default=None,
        max_length=256,
        title="Family Info",
        description="Family Info current child family data",
    )
    family_involvement: Optional[AlphaStr] = Field(
        default=None,
        max_length=128,
        title="Family Involvement",
        description="Family Involvement current child family data",
    )
    parenting_methods: Optional[ChildParentingMethodsEnum] = Field(
        default=None,
        title="Parenting Methods",
        description="Parenting Methods current child family data",
    )
    parental_attention_and_care: Optional[ChildParentalAttentionEnum] = Field(
        default=None,
        title="Parental Attention and Care",
        description="Parental Attention and Care current child family data",
    )
    child_id: PositiveInt = Field(
        default=...,
        title="Child ID",
        description="Child ID current child data",
    )


class ChildFamilyDataAddForm(ChildFamilyDataBasic):
    """
    Child Family Data add schema
    """

    ...


class ChildFamilyDataUpdateForm(ChildFamilyDataBasic):
    """
    Child Family Data update schema
    """

    ...


class ChildFamilyDataDetail(ChildFamilyDataBasic):
    """
    Child Family Data detail schema
    """

    id: PositiveInt = Field(
        default=..., title="ID", description="ID current child family data"
    )
    date: datetime.date = Field(
        default=..., title="Date", description="Date current child family data"
    )
