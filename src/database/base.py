from typing import ClassVar, Never, Callable

from sqlalchemy import SmallInteger, Column
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, declared_attr, ORMDescriptor, Mapped
from sqlalchemy.sql.elements import SQLCoreOperations


class Base(DeclarativeBase):
    """
    Base Model
    """

    id = Column(SmallInteger, primary_key=True)

    engine = create_async_engine(
        "postgresql+asyncpg://admin:qwerty@0.0.0.0:5432/star_track_bd",
        echo=True,
    )
    async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

    @declared_attr  # type:ignore
    def __tablename__(cls) -> str:
        """
        Autogenerate table name in database
        :return:
        """
        return "".join(
            f"_{i.lower()}" if i.isupper() else i for i in cls.__name__
        ).strip("_")
