from sqlalchemy import Column, INT
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
    AsyncAttrs,
)
from sqlalchemy.orm import DeclarativeBase, declared_attr

from src.settings import SETTINGS


class Base(AsyncAttrs, DeclarativeBase):
    """
    Base Model
    """

    __abstract__ = True

    id = Column(INT, primary_key=True, autoincrement=True)

    engine = create_async_engine(
        url=SETTINGS.DATABASE_URL.unicode_string(),
        echo=True,
        pool_size=5,
        max_overflow=15,
    )
    async_session_maker = async_sessionmaker(
        bind=engine,
        autocommit=False,
        class_=AsyncSession,
        autoflush=False,
        expire_on_commit=False,
    )

    @declared_attr  # type:ignore
    def __tablename__(cls) -> str:
        """
        Autogenerate table name in database
        :return:
        """
        return "".join(
            f"_{i.lower()}" if i.isupper() else i for i in cls.__name__
        ).strip("_")

    def __repr__(self):
        return f"{self.__tablename__}"
