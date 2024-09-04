from typing import List

from fastapi import APIRouter, Path, HTTPException
from fastapi.responses import ORJSONResponse
from fastapi_cache.decorator import cache
from pydantic import PositiveInt
from sqlalchemy.exc import NoResultFound
from starlette import status

from src.dependencies import UOWDep
from src.schemas.child_academic_data import (
    ChildAcademicDataDetail,
    ChildAcademicDataAddForm,
    ChildAcademicDataUpdateForm,
)
from src.services.child_academic_data import ChildAcademicDataService

# Initial child academic data router
router = APIRouter(
    prefix="/child_academic_data",
    tags=["Child Academic Data"],
    default_response_class=ORJSONResponse,
)


@router.get(
    path="",
    status_code=status.HTTP_200_OK,
    response_model=List[ChildAcademicDataDetail],
    name="Get list of child academic datas",
)
@cache(expire=120)
async def get_list_child_academic_datas(
    uow: UOWDep,
) -> List[ChildAcademicDataDetail]:
    """
    Get list of child academic datas
    :param uow:
    :return:
    """
    child_academic_datas = (
        await ChildAcademicDataService().get_child_academic_datas(uow=uow)
    )
    return child_academic_datas


@router.post(
    path="",
    status_code=status.HTTP_201_CREATED,
    response_model=ChildAcademicDataDetail,
    name="Add new child data",
)
async def add_new_child_academic_data(
    uow: UOWDep, add_form: ChildAcademicDataAddForm
) -> ChildAcademicDataDetail:
    """
    Add new child academic data
    :param uow:
    :param add_form:
    :return:
    """
    new_child_academic_data = (
        await ChildAcademicDataService().add_child_academic_data(
            uow=uow, child=add_form
        )
    )
    return new_child_academic_data


@router.get(
    path="/{child_academic_data_id}/",
    status_code=status.HTTP_200_OK,
    response_model=ChildAcademicDataDetail,
    name="Get child academic data by ID",
)
@cache(expire=120)
async def get_child_academic_data_by_id(
    uow: UOWDep, child_academic_data_id: PositiveInt = Path(default=..., ge=1)
) -> ChildAcademicDataDetail:
    """
    Get child academic data by ID
    :param child_academic_data_id:
    :param uow:
    :return:
    """
    try:
        child_academic_data = (
            await ChildAcademicDataService().get_child_academic_data(
                uow=uow, id=child_academic_data_id
            )
        )
        return child_academic_data
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Child academic data not found",
        )


@router.put(
    path="/{child_academic_data_id}/",
    status_code=status.HTTP_200_OK,
    response_model=ChildAcademicDataDetail,
    name="Update child academic data by ID",
)
async def update_child_data_by_id(
    uow: UOWDep,
    update_form: ChildAcademicDataUpdateForm,
    child_academic_data_id: PositiveInt = Path(default=..., ge=1),
) -> ChildAcademicDataDetail:
    """
    Update child academic data by ID
    :param child_academic_data_id:
    :param uow:
    :param update_form:
    :return:
    """
    try:
        update_child_academic_data = (
            await ChildAcademicDataService().update_child_academic_data(
                uow=uow, child=update_form, id=child_academic_data_id
            )
        )
        return update_child_academic_data
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Child academic data not found",
        )


@router.delete(
    path="/{child_academic_data_id}/",
    status_code=status.HTTP_200_OK,
    name="Delete academic child data by ID",
)
async def delete_child_academic_data_by_id(
    uow: UOWDep, child_academic_data_id: PositiveInt = Path(default=..., ge=1)
) -> dict:
    """
    Delete child academic data by ID
    :param uow:
    :param child_academic_data_id:
    :return:
    """
    try:
        await ChildAcademicDataService().delete_child_academic_data(
            uow=uow, id=child_academic_data_id
        )
        return {"msg": "Child academic data has been successfully removed"}
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Child academic data not found",
        )
