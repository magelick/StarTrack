from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker,
)

from src.database.models import Base
from pytest_asyncio import fixture as async_fixture

from src.repositories.models import (
    ChildRepository,
    ChildDataRepository,
    ChildFamilyDataRepository,
    ChildNutritionDataRepository,
    ChildAcademicDataRepository,
    ChildPhysicalDataRepository,
    ChildDevelopmentDataRepository,
    ChildHealthDataRepository,
    ChildMedicalDataRepository,
)


@async_fixture(scope="session")
async def db_engine():
    engine = create_async_engine(url="sqlite+aiosqlite:///test_db.sqlite")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@async_fixture(scope="session")
async def db_session(db_engine):
    """
    Fixture get async db session
    :param db_engine:
    :return:
    """
    async_session_maker = async_sessionmaker(
        bind=db_engine,
        autocommit=False,
        class_=AsyncSession,
        autoflush=False,
        expire_on_commit=False,
    )
    async with async_session_maker() as session:
        yield session


@async_fixture(scope="module")
async def get_child_repository(db_session):
    """
    Fixture which return ChildRepository
    :param db_session:
    :return:
    """
    return ChildRepository(session=db_session)


@async_fixture(scope="module")
async def get_child_data_repository(db_session):
    """
    Fixture which return ChildDataRepository
    :param db_session:
    :return:
    """
    return ChildDataRepository(session=db_session)


@async_fixture(scope="module")
async def get_child_health_data_repository(db_session):
    """
    Fixture which return ChildHealthDataRepository
    :param db_session:
    :return:
    """
    return ChildHealthDataRepository(session=db_session)


@async_fixture(scope="module")
async def get_child_medical_data_repository(db_session):
    """
    Fixture which return ChildMedicalDataRepository
    :param db_session:
    :return:
    """
    return ChildMedicalDataRepository(session=db_session)


@async_fixture(scope="module")
async def get_child_academic_data_repository(db_session):
    """
    Fixture which return ChildAcademicDataRepository
    :param db_session:
    :return:
    """
    return ChildAcademicDataRepository(session=db_session)


@async_fixture(scope="module")
async def get_child_development_data_repository(db_session):
    """
    Fixture which return ChildDevelopmentDataRepository
    :param db_session:
    :return:
    """
    return ChildDevelopmentDataRepository(session=db_session)


@async_fixture(scope="module")
async def get_child_physical_data_repository(db_session):
    """
    Fixture which return ChildPhysicalDataRepository
    :param db_session:
    :return:
    """
    return ChildPhysicalDataRepository(session=db_session)


@async_fixture(scope="module")
async def get_child_nutrition_data_repository(db_session):
    """
    Fixture which return ChildNutritionDataRepository
    :param db_session:
    :return:
    """
    return ChildNutritionDataRepository(session=db_session)


@async_fixture(scope="module")
async def get_child_family_data_repository(db_session):
    """
    Fixture which return ChildFamilyDataRepository
    :param db_session:
    :return:
    """
    return ChildFamilyDataRepository(session=db_session)
