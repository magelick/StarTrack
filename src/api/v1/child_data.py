from typing import List

from fastapi import APIRouter, Path, HTTPException
from fastapi.responses import ORJSONResponse
from fastapi_cache.decorator import cache
from pydantic import PositiveInt
from sqlalchemy.exc import NoResultFound
from starlette import status

from src.dependencies import UOWDep
from src.logger import logger
from src.schemas.child_data import (
    ChildDataDetail,
    ChildDataAddForm,
    ChildDataUpdateForm,
)
from src.services.child_data import ChildDataService

# Initial child data router
router = APIRouter(
    prefix="/child_data",
    tags=["Child Data"],
    default_response_class=ORJSONResponse,
)


@router.get(
    path="",
    status_code=status.HTTP_200_OK,
    response_model=List[ChildDataDetail],
    name="Get list of child datas",
)
@cache(expire=60)
async def get_list_child_datas(uow: UOWDep) -> List[ChildDataDetail]:
    """
    Get list of child datas
    :param uow:
    :return:
    """
    try:
        child_datas = await ChildDataService().get_child_datas(uow=uow)
        return child_datas
    except Exception as e:
        logger.error(e)
        return None


@router.post(
    path="",
    status_code=status.HTTP_201_CREATED,
    response_model=ChildDataDetail,
    name="Add new child data",
)
async def add_new_child_data(
    uow: UOWDep, add_form: ChildDataAddForm
) -> ChildDataDetail:
    """
    Add new child data
    :param uow:
    :param add_form:
    :return:
    """
    try:
        new_child_data = await ChildDataService().add_child_data(
            uow=uow, child_add_form=add_form
        )
        return new_child_data
    except Exception as e:
        logger.error(e)
        return None


@router.get(
    path="/{child_data_id}/",
    status_code=status.HTTP_200_OK,
    response_model=ChildDataDetail,
    name="Get child data by ID",
)
@cache(expire=60)
async def get_child_data_by_id(
    uow: UOWDep, child_data_id: PositiveInt = Path(default=..., ge=1)
) -> ChildDataDetail:
    """
    Get child data by ID
    :param child_data_id:
    :param uow:
    :return:
    """
    try:
        child_data = await ChildDataService().get_child_data(
            uow=uow, id=child_data_id
        )
        return child_data
    except (NoResultFound, Exception) as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Child data not found",
        )


@router.put(
    path="/{child_data_id}/",
    status_code=status.HTTP_200_OK,
    response_model=ChildDataDetail,
    name="Update child data by ID",
)
async def update_child_data_by_id(
    uow: UOWDep,
    update_form: ChildDataUpdateForm,
    child_data_id: PositiveInt = Path(default=..., ge=1),
) -> ChildDataDetail:
    """
    Update child data by ID
    :param uow:
    :param update_form:
    :param child_data_id:
    :return:
    """
    try:
        update_child_data = await ChildDataService().update_child_data(
            uow=uow, child_update_form=update_form, id=child_data_id
        )
        return update_child_data
    except (NoResultFound, Exception) as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Child data not found",
        )


@router.delete(
    path="/{child_data_id}/",
    status_code=status.HTTP_200_OK,
    name="Delete child data by ID",
)
async def delete_child_data_by_id(
    uow: UOWDep, child_data_id: PositiveInt = Path(default=..., ge=1)
) -> dict:
    """
    Delete child data by ID
    :param uow:
    :param child_data_id:
    :return:
    """
    try:
        await ChildDataService().delete_child_data(uow=uow, id=child_data_id)
        return {"msg": "Child has been successfully removed"}
    except (NoResultFound, Exception) as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Child data not found",
        )
