from typing import List

from fastapi import APIRouter, Path, HTTPException
from fastapi.responses import ORJSONResponse
from fastapi_cache.decorator import cache
from pydantic import PositiveInt
from sqlalchemy.exc import NoResultFound
from starlette import status

from src.dependencies import UOWDep
from src.schemas.child_family_data import (
    ChildFamilyDataDetail,
    ChildFamilyDataAddForm,
    ChildFamilyDataUpdateForm,
)
from src.services.child_family_data import ChildFamilyDataService

# Initial child family data router
router = APIRouter(
    prefix="/child_family_data",
    tags=["Child Family Data"],
    default_response_class=ORJSONResponse,
)


@router.get(
    path="",
    status_code=status.HTTP_200_OK,
    response_model=List[ChildFamilyDataDetail],
    name="Get list of family child datas",
)
@cache(expire=120)
async def get_list_child_family_datas(
    uow: UOWDep,
) -> List[ChildFamilyDataDetail]:
    """
    Get list of child family datas
    :param uow:
    :return:
    """
    child_family_datas = await ChildFamilyDataService().get_child_family_datas(
        uow=uow
    )
    return child_family_datas


@router.post(
    path="",
    status_code=status.HTTP_201_CREATED,
    response_model=ChildFamilyDataDetail,
    name="Add new child family data",
)
async def add_new_child_family_data(
    uow: UOWDep, add_form: ChildFamilyDataAddForm
) -> ChildFamilyDataDetail:
    """
    Add new child family data
    :param uow:
    :param add_form:
    :return:
    """
    new_child_family_data = (
        await ChildFamilyDataService().add_child_family_data(
            uow=uow, child=add_form
        )
    )
    return new_child_family_data


@router.get(
    path="/{child_family_data_id}/",
    status_code=status.HTTP_200_OK,
    response_model=ChildFamilyDataDetail,
    name="Get child family data by ID",
)
@cache(expire=120)
async def get_child_family_data_by_id(
    uow: UOWDep, child_family_data_id: PositiveInt = Path(default=..., ge=1)
) -> ChildFamilyDataDetail:
    """
    Get child family data by ID
    :param child_family_data_id:
    :param uow:
    :return:
    """
    try:
        child_family_data = (
            await ChildFamilyDataService().get_child_family_data(
                uow=uow, id=child_family_data_id
            )
        )
        return child_family_data
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Child family data not found",
        )


@router.put(
    path="/{child_family_data_id}/",
    status_code=status.HTTP_200_OK,
    response_model=ChildFamilyDataDetail,
    name="Update child family data by ID",
)
async def update_child_family_data_by_id(
    uow: UOWDep,
    update_form: ChildFamilyDataUpdateForm,
    child_family_data_id: PositiveInt = Path(default=..., ge=1),
) -> ChildFamilyDataDetail:
    """
    Update child family data by ID
    :param uow:
    :param update_form:
    :param child_family_data_id:
    :return:
    """
    try:
        update_child_family_data = (
            await ChildFamilyDataService().update_child_family_data(
                uow=uow, child=update_form, id=child_family_data_id
            )
        )
        return update_child_family_data
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Child family data not found",
        )


@router.delete(
    path="/{child_family_data_id}/",
    status_code=status.HTTP_200_OK,
    name="Delete child family data by ID",
)
async def delete_child_family_data_by_id(
    uow: UOWDep, child_family_data_id: PositiveInt = Path(default=..., ge=1)
) -> dict:
    """
    Delete child family data by ID
    :param uow:
    :param child_family_data_id:
    :return:
    """
    try:
        await ChildFamilyDataService().delete_child_family_data(
            uow=uow, id=child_family_data_id
        )
        return {"msg": "Child family data has been successfully removed"}
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Child family data not found",
        )
