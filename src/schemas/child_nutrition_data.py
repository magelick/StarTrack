import datetime
from typing import Optional

from pydantic import Field, PositiveInt

from src.schemas.base import DTO
from src.schemas.custom_types import AlphaStr


class ChildNutritionDataBasic(DTO):
    """
    Basic Child Nutrition Data schema
    """

    dietary_info: Optional[AlphaStr] = Field(
        default=None,
        title="Dietary Info",
        description="Dietary Info current child nutrition data",
    )
    snacking_habits: Optional[bool] = Field(
        default=True,
        title="Snacking Habits",
        description="Snacking Habits current child nutrition data",
    )
    beverage_consumption: Optional[bool] = Field(
        default=True,
        title="Beverage Consumption",
        description="Beverage Consumption current child nutrition data",
    )
    supplements_or_vitamins: Optional[AlphaStr] = Field(
        default=None,
        max_length=256,
        title="Supplements or Vitamins",
        description="Supplements or Vitamins current child nutrition data",
    )
    reactions_to_food: Optional[AlphaStr] = Field(
        default=None,
        max_length=256,
        title="Reactions to Food",
        description="Reactions to Food current child nutrition data",
    )
    allergies_and_intolerances: Optional[AlphaStr] = Field(
        default=None,
        max_length=256,
        title="Allergies and Intolerances",
        description="Allergies and Intolerances current child nutrition data",
    )
    child_id: PositiveInt = Field(
        default=...,
        title="Child ID",
        description="Child ID current child nutrition data",
    )


class ChildNutritionDataAddForm(ChildNutritionDataBasic):
    """
    Child Nutrition Data add schema
    """

    ...


class ChildNutritionDataUpdateForm(ChildNutritionDataBasic):
    """
    Child Nutrition Data update schema
    """

    ...


class ChildNutritionDataDetail(ChildNutritionDataBasic):
    """
    Child Nutrition Data detail schema
    """

    id: PositiveInt = Field(
        default=..., title="ID", description="ID current child nutrition data"
    )
    date: datetime.date = Field(
        default=...,
        title="Date",
        description="Date current child nutrition data",
    )
