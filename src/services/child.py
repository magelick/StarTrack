from typing import List

from src.unit_of_work import AbstractUnitOfWork
from src.schemas.child import ChildDetail, ChildAddForm, ChildUpdateForm


class ChildService:
    """
    Child service
    """

    async def get_children(self, uow: AbstractUnitOfWork) -> List[ChildDetail]:
        """
        Get all children
        :param uow:
        :return:
        """
        async with uow:
            children = await uow.children.get_all()

            return [
                ChildDetail.model_validate(child, from_attributes=True)
                for child in children
            ]

    async def add_child(
        self, uow: AbstractUnitOfWork, child: ChildAddForm
    ) -> ChildDetail:
        """
        Add new child
        :param uow:
        :param child:
        :return:
        """
        async with uow:
            new_child = await uow.children.add_one(child.model_dump())
            await uow.commit()

            return ChildDetail.model_validate(new_child, from_attributes=True)

    async def get_child(
        self, uow: AbstractUnitOfWork, **filter_by
    ) -> ChildDetail:
        """
        Get child by some filter
        :param uow:
        :return:
        """
        async with uow:
            child = await uow.children.get_one(**filter_by)

            return ChildDetail.model_validate(child, from_attributes=True)

    async def update_child(
        self, uow: AbstractUnitOfWork, child: ChildUpdateForm, **filter_by
    ) -> ChildDetail:
        """
        Update some child
        :param uow:
        :param child:
        :return:
        """
        async with uow:
            update_child = await uow.children.update_one(
                child.model_dump(), **filter_by
            )
            await uow.commit()

            return ChildDetail.model_validate(
                update_child, from_attributes=True
            )

    async def delete_child(self, uow: AbstractUnitOfWork, **filter_by):
        """
        Delete some child
        :param uow:
        :return:
        """
        async with uow:
            await uow.children.delete_one(**filter_by)
            await uow.commit()
