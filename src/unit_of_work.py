from abc import ABC, abstractmethod
from typing import Type

from src.database.models import Base
from src.repositories.models import (
    UserRepository,
    ChildRepository,
    ChildDataRepository,
    ChildMedicalDataRepository,
    ChildHealthDataRepository,
    ChildDevelopmentDataRepository,
    ChildPhysicalDataRepository,
    ChildAcademicDataRepository,
    ChildFamilyDataRepository,
    ChildNutritionDataRepository,
)


class IUnitOfWork(ABC):
    """
    Abstract class for Unit Of Work pattern
    """

    users: Type[UserRepository]
    children: Type[ChildRepository]
    child_datas: Type[ChildDataRepository]
    child_medical_datas: Type[ChildMedicalDataRepository]
    child_health_datas: Type[ChildHealthDataRepository]
    child_development_datas: Type[ChildDevelopmentDataRepository]
    child_physical_datas: Type[ChildPhysicalDataRepository]
    child_academic_datas: Type[ChildAcademicDataRepository]
    child_family_datas: Type[ChildFamilyDataRepository]
    child_nutrition_datas: Type[ChildNutritionDataRepository]

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    async def __aenter__(self):
        pass

    @abstractmethod
    async def __aexit__(self, *args):
        pass

    @abstractmethod
    async def commit(self):
        pass

    @abstractmethod
    async def rollback(self):
        pass


class UnitOfWork:
    """
    Basic class for Unit Of Work pattern
    """

    def __init__(self):
        self.session_factory = Base.async_session_maker

    async def __aenter__(self):
        self._session = self.session_factory()

        self.users = UserRepository(self._session)
        self.children = ChildRepository(self._session)
        self.child_datas = ChildDataRepository(self._session)
        self.child_medical_datas = ChildMedicalDataRepository(self._session)
        self.child_health_datas = ChildHealthDataRepository(self._session)
        self.child_development_datas = ChildDevelopmentDataRepository(
            self._session
        )
        self.child_physical_datas = ChildPhysicalDataRepository(self._session)
        self.child_academic_datas = ChildAcademicDataRepository(self._session)
        self.child_family_datas = ChildFamilyDataRepository(self._session)
        self.child_nutrition_datas = ChildNutritionDataRepository(
            self._session
        )

    async def __aexit__(self, *args):
        await self.rollback()
        await self._session.close()

    async def commit(self):
        await self._session.commit()

    async def rollback(self):
        await self._session.rollback()
