from src.database.models import (
    User,
    Child,
    ChildData,
    ChildMedicalData,
    ChildHealthData,
    ChildDevelopmentData,
    ChildPhysicalData,
    ChildAcademicData,
    ChildFamilyData,
    ChildNutritionData,
)
from src.repositories.base import SQLAlchemyRepository


class UserRepository(SQLAlchemyRepository):
    """
    Repository for User model
    """

    model = User


class ChildRepository(SQLAlchemyRepository):
    """
    Repository for Child model
    """

    model = Child


class ChildDataRepository(SQLAlchemyRepository):
    """
    Repository for Child Data model
    """

    model = ChildData


class ChildMedicalDataRepository(SQLAlchemyRepository):
    """
    Repository for Child Medical Data model
    """

    model = ChildMedicalData


class ChildHealthDataRepository(SQLAlchemyRepository):
    """
    Repository for Child Health Data model
    """

    model = ChildHealthData


class ChildDevelopmentDataRepository(SQLAlchemyRepository):
    """
    Repository for Child Development Data model
    """

    model = ChildDevelopmentData


class ChildPhysicalDataRepository(SQLAlchemyRepository):
    """
    Repository for Child Physical Data model
    """

    model = ChildPhysicalData


class ChildAcademicDataRepository(SQLAlchemyRepository):
    """
    Repository for Child Academic Data model
    """

    model = ChildAcademicData


class ChildFamilyDataRepository(SQLAlchemyRepository):
    """
    Repository for Child Family Data model
    """

    model = ChildFamilyData


class ChildNutritionDataRepository(SQLAlchemyRepository):
    """
    Repository for Child Nutrition Data model
    """

    model = ChildNutritionData
