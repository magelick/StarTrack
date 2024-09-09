import datetime
from typing import Optional

from pydantic import Field, PositiveInt

from src.schemas.base import DTO
from src.database.enums import ChildBloodTypeEnum


class ChildMedicalDataBasic(DTO):
    """
    Basic Child Medical Data schema
    """

    vaccinations: Optional[str] = Field(
        default=None,
        title="Vaccinations",
        description="Vaccinations current child medical data",
    )
    medications: Optional[str] = Field(
        default=None,
        title="Medications",
        description="Medications current child medical data",
    )
    procedures: Optional[str] = Field(
        default=None,
        title="Procedures",
        description="Procedures current child medical data",
    )
    blood_tests: Optional[int] = Field(
        default=None,
        title="Blood Tests",
        description="Blood Tests current child medical data",
    )
    urine_tests: Optional[int] = Field(
        default=None,
        title="Urine Tests",
        description="Urine Tests current child medical data",
    )
    blood_type: Optional[ChildBloodTypeEnum] = Field(
        default=None,
        title="Blood Type",
        description="Blood Type current child medical data",
    )
    child_id: PositiveInt = Field(
        default=...,
        title="Child ID",
        description="Child ID current child medical data",
    )


class ChildMedicalDataAddForm(ChildMedicalDataBasic):
    """
    Child Medical Data add schema
    """

    ...


class ChildMedicalDataUpdateForm(ChildMedicalDataBasic):
    """
    Child Medical Data update schema
    """

    ...


class ChildMedicalDataDetail(ChildMedicalDataBasic):
    """
    Child Medical Data detail schema
    """

    id: PositiveInt = Field(
        default=..., title="ID", description="ID current child medical data"
    )
    rohrer_index: Optional[float] = Field(
        default=None,
        title="Rohrer Index",
        description="Rohrer Index current child medical data",
    )
    bsa_index: Optional[float] = Field(
        default=None,
        title="BSA Index",
        description="BSA Index current child medical dat",
    )
    date: datetime.date = Field(
        default=...,
        title="Date",
        description="Date current child medical data",
    )
