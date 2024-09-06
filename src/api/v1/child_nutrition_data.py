from typing import List

from fastapi import APIRouter, Path, HTTPException
from fastapi.responses import ORJSONResponse
from fastapi_cache.decorator import cache
from pydantic import PositiveInt
from sqlalchemy.exc import NoResultFound
from starlette import status

from src.dependencies import UOWDep
from src.schemas.child_nutrition_data import (
    ChildNutritionDataDetail,
    ChildNutritionDataAddForm,
    ChildNutritionDataUpdateForm,
)
from src.services.child_nutrition_data import ChildNutritionDataService

# Initial child nutrition data router
router = APIRouter(
    prefix="/child_nutrition_data",
    tags=["Child Nutrition Data"],
    default_response_class=ORJSONResponse,
)


@router.get(
    path="",
    status_code=status.HTTP_200_OK,
    response_model=List[ChildNutritionDataDetail],
    name="Get list of child nutrition datas",
)
@cache(expire=120)
async def get_list_child_nutrition_datas(
    uow: UOWDep,
) -> List[ChildNutritionDataDetail]:
    """
    Get list of child nutrition datas
    :param uow:
    :return:
    """
    child_nutrition_datas = (
        await ChildNutritionDataService().get_child_nutrition_datas(uow=uow)
    )
    return child_nutrition_datas


@router.post(
    path="",
    status_code=status.HTTP_201_CREATED,
    response_model=ChildNutritionDataDetail,
    name="Add new child nutrition data",
)
async def add_new_child_nutrition_data(
    uow: UOWDep, add_form: ChildNutritionDataAddForm
) -> ChildNutritionDataDetail:
    """
    Add new child nutrition data
    :param uow:
    :param add_form:
    :return:
    """
    new_child_nutrition_data = (
        await ChildNutritionDataService().add_child_nutrition_data(
            uow=uow, child=add_form
        )
    )
    return new_child_nutrition_data


@router.get(
    path="/{child_nutrition_data_id}/",
    status_code=status.HTTP_200_OK,
    response_model=ChildNutritionDataDetail,
    name="Get child nutrition data by ID",
)
@cache(expire=120)
async def get_child_nutrition_data_by_id(
    uow: UOWDep, child_nutrition_data_id: PositiveInt = Path(default=..., ge=1)
) -> ChildNutritionDataDetail:
    """
    Get child nutrition data by ID
    :param child_nutrition_data_id:
    :param uow:
    :return:
    """
    try:
        child_nutrition_data = (
            await ChildNutritionDataService().get_child_nutrition_data(
                uow=uow, id=child_nutrition_data_id
            )
        )
        return child_nutrition_data
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Child nutrition data not found",
        )


@router.put(
    path="/{child_nutrition_data_id}/",
    status_code=status.HTTP_200_OK,
    response_model=ChildNutritionDataDetail,
    name="Update child nutrition data by ID",
)
async def update_child_nutrition_data_by_id(
    uow: UOWDep,
    update_form: ChildNutritionDataUpdateForm,
    child_nutrition_data_id: PositiveInt = Path(default=..., ge=1),
) -> ChildNutritionDataDetail:
    """
    Update child nutrition data by ID
    :param uow:
    :param update_form:
    :param child_nutrition_data_id:
    :return:
    """
    try:
        update_child_data = (
            await ChildNutritionDataService().update_child_nutrition_data(
                uow=uow, child=update_form, id=child_nutrition_data_id
            )
        )
        return update_child_data
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Child nutrition data not found",
        )


@router.delete(
    path="/{child_nutrition_data_id}/",
    status_code=status.HTTP_200_OK,
    name="Delete child nutrition data by ID",
)
async def delete_child_nutrition_data_by_id(
    uow: UOWDep, child_nutrition_data_id: PositiveInt = Path(default=..., ge=1)
) -> dict:
    """
    Delete child nutrition data by ID
    :param uow:
    :param child_nutrition_data_id:
    :return:
    """
    try:
        await ChildNutritionDataService().delete_child_nutrition_data(
            uow=uow, id=child_nutrition_data_id
        )
        return {"msg": "Child nutrition data has been successfully removed"}
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Child nutrition data not found",
        )
