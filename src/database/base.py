from sqlalchemy import Column, SMALLINT
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, declared_attr

from src.settings import SETTINGS


class Base(DeclarativeBase):
    """
    Base Model
    """

    id = Column(SMALLINT, primary_key=True)

    engine = create_async_engine(
        url=SETTINGS.DATABASE_URL.unicode_string(),
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
