from typing import List

from fastapi import APIRouter, Path, HTTPException
from fastapi.responses import ORJSONResponse
from fastapi_cache.decorator import cache
from pydantic import PositiveInt
from sqlalchemy.exc import NoResultFound
from starlette import status

from src.dependencies import UOWDep
from src.schemas.child_physical_data import (
    ChildPhysicalDataDetail,
    ChildPhysicalDataAddForm,
    ChildPhysicalDataUpdateForm,
)
from src.services.child_physical_data import ChildPhysicalDataService

# Initial child physical data router
router = APIRouter(
    prefix="/child_physical_data",
    tags=["Child Physical Data"],
    default_response_class=ORJSONResponse,
)


@router.get(
    path="",
    status_code=status.HTTP_200_OK,
    response_model=List[ChildPhysicalDataDetail],
    name="Get list of child datas",
)
@cache(expire=120)
async def get_list_child_physical_datas(
    uow: UOWDep,
) -> List[ChildPhysicalDataDetail]:
    """
    Get list of child physical datas
    :param uow:
    :return:
    """
    child_physical_datas = (
        await ChildPhysicalDataService().get_child_physical_datas(uow=uow)
    )
    return child_physical_datas


@router.post(
    path="",
    status_code=status.HTTP_201_CREATED,
    response_model=ChildPhysicalDataDetail,
    name="Add new child physical data",
)
async def add_new_child_physical_data(
    uow: UOWDep, add_form: ChildPhysicalDataAddForm
) -> ChildPhysicalDataDetail:
    """
    Add new child physical data
    :param uow:
    :param add_form:
    :return:
    """
    new_child_physical_data = (
        await ChildPhysicalDataService().add_child_physical_data(
            uow=uow, child=add_form
        )
    )
    return new_child_physical_data


@router.get(
    path="/{child_physical_data_id}/",
    status_code=status.HTTP_200_OK,
    response_model=ChildPhysicalDataDetail,
    name="Get child physical data by ID",
)
@cache(expire=120)
async def get_child_physical_data_by_id(
    uow: UOWDep, child_physical_data_id: PositiveInt = Path(default=..., ge=1)
) -> ChildPhysicalDataDetail:
    """
    Get child physical data by ID
    :param child_physical_data_id:
    :param uow:
    :return:
    """
    try:
        child_physical_data = (
            await ChildPhysicalDataService().get_child_physical_data(
                uow=uow, id=child_physical_data_id
            )
        )
        return child_physical_data
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Child physical data not found",
        )


@router.put(
    path="/{child_physical_data_id}/",
    status_code=status.HTTP_200_OK,
    response_model=ChildPhysicalDataDetail,
    name="Update child physical data by ID",
)
async def update_child_data_by_id(
    uow: UOWDep,
    update_form: ChildPhysicalDataUpdateForm,
    child_physical_data_id: PositiveInt = Path(default=..., ge=1),
) -> ChildPhysicalDataDetail:
    """
    Update child physical data by ID
    :param uow:
    :param update_form:
    :param child_physical_data_id:
    :return:
    """
    try:
        update_child_physical_data = (
            await ChildPhysicalDataService().update_child_physical_data(
                uow=uow, child=update_form, id=child_physical_data_id
            )
        )
        return update_child_physical_data
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Child physical data not found",
        )


@router.delete(
    path="/{child_physical_data_id}/",
    status_code=status.HTTP_200_OK,
    name="Delete child data by ID",
)
async def delete_child_physical_data_by_id(
    uow: UOWDep, child_physical_data_id: PositiveInt = Path(default=..., ge=1)
) -> dict:
    """
    Delete child physical data by ID
    :param uow:
    :param child_physical_data_id:
    :return:
    """
    try:
        await ChildPhysicalDataService().delete_child_physical_data(
            uow=uow, id=child_physical_data_id
        )
        return {"msg": "Child physical data has been successfully removed"}
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Child physical data not found",
        )
