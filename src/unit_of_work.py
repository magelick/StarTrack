from abc import ABC, abstractmethod

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


class AbstractUnitOfWork(ABC):
    """
    Abstract class for Unit Of Work pattern
    """

    users: UserRepository
    children: ChildRepository
    child_datas: ChildDataRepository
    child_medical_datas: ChildMedicalDataRepository
    child_health_datas: ChildHealthDataRepository
    child_development_datas: ChildDevelopmentDataRepository
    child_physical_datas: ChildPhysicalDataRepository
    child_academic_datas: ChildAcademicDataRepository
    child_family_datas: ChildFamilyDataRepository
    child_nutrition_datas: ChildNutritionDataRepository

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

    @abstractmethod
    async def refresh(self, instance):
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

    async def refresh(self, instance: object):
        await self._session.refresh(instance=instance)
