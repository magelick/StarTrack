from typing import List

from fastapi import APIRouter, Path, HTTPException
from fastapi.responses import ORJSONResponse
from fastapi_cache.decorator import cache
from pydantic import PositiveInt
from sqlalchemy.exc import NoResultFound
from starlette import status

from src.dependencies import UOWDep
from src.logger import logger
from src.schemas.child_health_data import (
    ChildHealthDataDetail,
    ChildHealthDataAddForm,
    ChildHealthDataUpdateForm,
)
from src.services.child_health_data import ChildHealthDataService

# Initial child health data router
router = APIRouter(
    prefix="/child_health_data",
    tags=["Child Health Data"],
    default_response_class=ORJSONResponse,
)


@router.get(
    path="",
    status_code=status.HTTP_200_OK,
    response_model=List[ChildHealthDataDetail],
    name="Get list of child health datas",
)
@cache(expire=60)
async def get_list_child_health_datas(
    uow: UOWDep,
) -> List[ChildHealthDataDetail]:
    """
    Get list of child health datas
    :param uow:
    :return:
    """
    try:
        child_health_datas = (
            await ChildHealthDataService().get_child_health_datas(uow=uow)
        )
        return child_health_datas
    except Exception as e:
        logger.error(e)
        return None


@router.post(
    path="",
    status_code=status.HTTP_201_CREATED,
    response_model=ChildHealthDataDetail,
    name="Add new child health data",
)
async def add_new_child_health_data(
    uow: UOWDep, add_form: ChildHealthDataAddForm
) -> ChildHealthDataDetail:
    """
    Add new child health data
    :param uow:
    :param add_form:
    :return:
    """
    try:
        new_child_health_data = (
            await ChildHealthDataService().add_child_health_data(
                uow=uow, child=add_form
            )
        )
        return new_child_health_data
    except Exception as e:
        logger.error(e)
        return None


@router.get(
    path="/{child_health_data_id}/",
    status_code=status.HTTP_200_OK,
    response_model=ChildHealthDataDetail,
    name="Get child health data by ID",
)
@cache(expire=60)
async def get_child_health_data_by_id(
    uow: UOWDep, child_data_id: PositiveInt = Path(default=..., ge=1)
) -> ChildHealthDataDetail:
    """
    Get child health data by ID
    :param child_data_id:
    :param uow:
    :return:
    """
    try:
        child_health_data = (
            await ChildHealthDataService().get_child_health_data(
                uow=uow, id=child_data_id
            )
        )
        return child_health_data
    except (NoResultFound, Exception) as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Child health data not found",
        )


@router.put(
    path="/{child_health_data_id}/",
    status_code=status.HTTP_200_OK,
    response_model=ChildHealthDataDetail,
    name="Update child health data by ID",
)
async def update_child_data_by_id(
    uow: UOWDep,
    update_form: ChildHealthDataUpdateForm,
    child_health_data_id: PositiveInt = Path(default=..., ge=1),
) -> ChildHealthDataDetail:
    """
    Update child health data by ID
    :param uow:
    :param update_form:
    :param child_health_data_id:
    :return:
    """
    try:
        update_child_health_data = (
            await ChildHealthDataService().update_child_data(
                uow=uow, child=update_form, id=child_health_data_id
            )
        )
        return update_child_health_data
    except (NoResultFound, Exception) as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Child health data not found",
        )


@router.delete(
    path="/{child_health_data_id}/",
    status_code=status.HTTP_200_OK,
    name="Delete child health data by ID",
)
async def delete_child_health_data_by_id(
    uow: UOWDep, child_health_data_id: PositiveInt = Path(default=..., ge=1)
) -> dict:
    """
    Delete child health data by ID
    :param uow:
    :param child_health_data_id:
    :return:
    """
    try:
        await ChildHealthDataService().delete_child_health_data(
            uow=uow, id=child_health_data_id
        )
        return {"msg": "Child health data has been successfully removed"}
    except (NoResultFound, Exception) as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Child health data not found",
        )
