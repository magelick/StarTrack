from abc import ABC, abstractmethod
from typing import Type

from sqlalchemy import insert, select, update, delete, Executable
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Base


class AbstractRepository(ABC):
    @abstractmethod
    async def add_one(self, data: dict):
        raise NotImplementedError

    @abstractmethod
    async def get_all(self):
        raise NotImplementedError

    @abstractmethod
    async def get_one(self):
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    model: Type[Base] = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_one(self, data: dict):
        stmt: Executable = insert(self.model).values(**data)
        res = await self.session.execute(stmt)
        return res

    async def update_one(self, data: dict, **filter_by):
        stmt: Executable = (
            update(self.model).values(**data).filter_by(**filter_by)
        )
        res = await self.session.execute(stmt)
        return res

    async def get_all(self):
        stmt: Executable = select(self.model)
        res = await self.session.execute(stmt)
        return res.all()

    async def get_one(self, **filter_by):
        stmt: Executable = select(self.model).filter_by(**filter_by)
        res = await self.session.execute(stmt)
        return res

    async def delete_one(self, **filter_by):
        stmt: Executable = delete(self.model).filter_by(**filter_by)
        await self.session.execute(stmt)
