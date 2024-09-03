from typing import List

from src.unit_of_work import AbstractUnitOfWork
from src.schemas.child_nutrition_data import (
    ChildNutritionDataDetail,
    ChildNutritionDataAddForm,
    ChildNutritionDataUpdateForm,
)


class ChildNutritionDataService:
    """
    Child Nutrition Data service
    """

    async def get_child_nutrition_datas(
        self, uow: AbstractUnitOfWork
    ) -> List[ChildNutritionDataDetail]:
        """
        Get all child nutrition datas
        :param uow:
        :return:
        """
        async with uow:
            child_nutrition_datas = await uow.child_nutrition_datas.get_all()
            return [
                ChildNutritionDataDetail.model_validate(
                    child_nutrition_data, from_attributes=True
                )
                for child_nutrition_data in child_nutrition_datas
            ]

    async def add_child_nutrition_data(
        self, uow: AbstractUnitOfWork, child: ChildNutritionDataAddForm
    ) -> ChildNutritionDataDetail:
        """
        Add new child nutrition data
        :param uow:
        :param child:
        :return:
        """
        async with uow:
            new_child_nutrition_data = await uow.child_nutrition_datas.add_one(
                child.model_dump()
            )
            await uow.commit()
            return ChildNutritionDataDetail.model_validate(
                new_child_nutrition_data, from_attributes=True
            )

    async def get_child_nutrition_data(
        self, uow: AbstractUnitOfWork, **filter_by
    ) -> ChildNutritionDataDetail:
        """
        Get child nutrition data by some filter
        :param uow:
        :return:
        """
        async with uow:
            child_nutrition_data = await uow.child_nutrition_datas.get_one(
                **filter_by
            )
            return ChildNutritionDataDetail.model_validate(
                child_nutrition_data, from_attributes=True
            )

    async def update_child_nutrition_data(
        self,
        uow: AbstractUnitOfWork,
        child: ChildNutritionDataUpdateForm,
        **filter_by
    ) -> ChildNutritionDataDetail:
        """
        Update some child nutrition data
        :param uow:
        :param child:
        :return:
        """
        async with uow:
            update_child_nutrition_data = (
                await uow.child_nutrition_datas.update_one(
                    child.model_dump(), **filter_by
                )
            )
            await uow.commit()
            return ChildNutritionDataDetail.model_validate(
                update_child_nutrition_data, from_attributes=True
            )

    async def delete_child_nutrition_data(
        self, uow: AbstractUnitOfWork, **filter_by
    ):
        """
        Delete some child nutrition data
        :param uow:
        :return:
        """
        async with uow:
            await uow.child_datas.delete_one(**filter_by)
            await uow.commit()
