from typing import List

from fastapi import APIRouter, Path, HTTPException
from fastapi.responses import ORJSONResponse
from fastapi_cache.decorator import cache
from pydantic import PositiveInt
from sqlalchemy.exc import NoResultFound
from starlette import status

from src.dependencies import UOWDep
from src.schemas.child_development_data import (
    ChildDevelopmentDataDetail,
    ChildDevelopmentDataAddForm,
    ChildDevelopmentDataUpdateForm,
)
from src.services.child_development_data import ChildDevelopmentDataService

# Initial child development data router
router = APIRouter(
    prefix="/child_development_data",
    tags=["Child Development Data"],
    default_response_class=ORJSONResponse,
)


@router.get(
    path="",
    status_code=status.HTTP_200_OK,
    response_model=List[ChildDevelopmentDataDetail],
    name="Get list of child development datas",
)
@cache(expire=120)
async def get_list_child_development_datas(
    uow: UOWDep,
) -> List[ChildDevelopmentDataDetail]:
    """
    Get list of child development datas
    :param uow:
    :return:
    """
    child_development_datas = (
        await ChildDevelopmentDataService().get_child_development_datas(
            uow=uow
        )
    )
    return child_development_datas


@router.post(
    path="",
    status_code=status.HTTP_201_CREATED,
    response_model=ChildDevelopmentDataDetail,
    name="Add new child development data",
)
async def add_new_child_development_data(
    uow: UOWDep, add_form: ChildDevelopmentDataAddForm
) -> ChildDevelopmentDataDetail:
    """
    Add new child development data
    :param uow:
    :param add_form:
    :return:
    """
    new_child_development_data = (
        await ChildDevelopmentDataService().add_child_development_data(
            uow=uow, child=add_form
        )
    )
    return new_child_development_data


@router.get(
    path="/{child_development_data_id}/",
    status_code=status.HTTP_200_OK,
    response_model=ChildDevelopmentDataDetail,
    name="Get child development data by ID",
)
@cache(expire=120)
async def get_child_development_data_by_id(
    uow: UOWDep,
    child_development_data_id: PositiveInt = Path(default=..., ge=1),
) -> ChildDevelopmentDataDetail:
    """
    Get child development data by ID
    :param child_development_data_id:
    :param uow:
    :return:
    """
    try:
        child_development_data = (
            await ChildDevelopmentDataService().get_child_development_data(
                uow=uow, id=child_development_data_id
            )
        )
        return child_development_data
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Child development data not found",
        )


@router.put(
    path="/{child_development_data_id}/",
    status_code=status.HTTP_200_OK,
    response_model=ChildDevelopmentDataDetail,
    name="Update child development data by ID",
)
async def update_child_development_data_by_id(
    uow: UOWDep,
    update_form: ChildDevelopmentDataUpdateForm,
    child_development_data_id: PositiveInt = Path(default=..., ge=1),
) -> ChildDevelopmentDataDetail:
    """
    Update child development data by ID
    :param uow:
    :param update_form:
    :param child_development_data_id:
    :return:
    """
    try:
        update_child_development_data = (
            await ChildDevelopmentDataService().update_child_development_data(
                uow=uow, child=update_form, id=child_development_data_id
            )
        )
        return update_child_development_data
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Child development data not found",
        )


@router.delete(
    path="/{child_development_data_id}/",
    status_code=status.HTTP_200_OK,
    name="Delete child development data by ID",
)
async def delete_child_development_data_by_id(
    uow: UOWDep,
    child_development_data_id: PositiveInt = Path(default=..., ge=1),
) -> dict:
    """
    Delete child development data by ID
    :param uow:
    :param child_development_data_id:
    :return:
    """
    try:
        await ChildDevelopmentDataService().delete_child_development_data(
            uow=uow, id=child_development_data_id
        )
        return {"msg": "Child development data has been successfully removed"}
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Child development data data not found",
        )
