import datetime
from typing import Optional

from pydantic import Field, PositiveInt

from src.database.enums import ChildDevelopmentEnum, ChildCommunicationEnum
from src.schemas.base import DTO


class ChildDevelopmentDataBasic(DTO):
    """
    Basic Child Development Data schema
    """

    peer_interactions: Optional[ChildDevelopmentEnum] = Field(
        default=None, title="", description=" current child development data"
    )
    communication_skills: Optional[ChildCommunicationEnum] = Field(
        default=None, title="", description=" current child development data"
    )
    attention_level: Optional[ChildDevelopmentEnum] = Field(
        default=None, title="", description=" current child development data"
    )
    memory_level: Optional[ChildDevelopmentEnum] = Field(
        default=None, title="", description=" current child development data"
    )
    problem_solving_skills: Optional[ChildDevelopmentEnum] = Field(
        default=None, title="", description=" current child development data"
    )
    cognitive_tests: Optional[ChildDevelopmentEnum] = Field(
        default=None, title="", description=" current child development data"
    )
    emotional_tests: Optional[ChildDevelopmentEnum] = Field(
        default=None, title="", description=" current child development data"
    )
    child_id: PositiveInt = Field(
        default=...,
        title="Child ID",
        description="Child ID current child development data",
    )


class ChildDevelopmentDataAddForm(ChildDevelopmentDataBasic):
    """
    Child Development Data add schema
    """

    ...


class ChildDevelopmentDataUpdateForm(ChildDevelopmentDataBasic):
    """
    Child Development Data update schema
    """

    ...


class ChildDevelopmentDataDetail(ChildDevelopmentDataBasic):
    """
    Child Development Data detail schema
    """

    id: PositiveInt = Field(
        default=...,
        title="ID",
        description="ID current child development data",
    )
    date: datetime.date = Field(
        default=...,
        title="Date",
        description="Date current child development data",
    )
