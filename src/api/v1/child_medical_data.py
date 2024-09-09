from typing import List

from fastapi import APIRouter, Path, HTTPException
from fastapi.responses import ORJSONResponse
from fastapi_cache.decorator import cache
from pydantic import PositiveInt
from sqlalchemy.exc import NoResultFound
from starlette import status

from src.dependencies import UOWDep
from src.schemas.child_medical_data import (
    ChildMedicalDataDetail,
    ChildMedicalDataAddForm,
    ChildMedicalDataUpdateForm,
)
from src.services.child_medical_data import ChildMedicalDataService

# Initial child medical data router
router = APIRouter(
    prefix="/child_medical_data",
    tags=["Child Medical Data"],
    default_response_class=ORJSONResponse,
)


@router.get(
    path="",
    status_code=status.HTTP_200_OK,
    response_model=List[ChildMedicalDataDetail],
    name="Get list of child medical datas",
)
@cache(expire=120)
async def get_list_child_medical_datas(
    uow: UOWDep,
) -> List[ChildMedicalDataDetail]:
    """
    Get list of child datas
    :param uow:
    :return:
    """
    child_medical_datas = (
        await ChildMedicalDataService().get_child_medical_datas(uow=uow)
    )
    return child_medical_datas


@router.post(
    path="",
    status_code=status.HTTP_201_CREATED,
    response_model=ChildMedicalDataDetail,
    name="Add new child medical data",
)
async def add_new_child_medical_data(
    uow: UOWDep, add_form: ChildMedicalDataAddForm
) -> ChildMedicalDataDetail:
    """
    Add new child medical data
    :param uow:
    :param add_form:
    :return:
    """
    new_child_medical_data = (
        await ChildMedicalDataService().add_child_medical_data(
            uow=uow, child=add_form
        )
    )
    return new_child_medical_data


@router.get(
    path="/{child_medical_data_id}/",
    status_code=status.HTTP_200_OK,
    response_model=ChildMedicalDataDetail,
    name="Get child medical data by ID",
)
@cache(expire=120)
async def get_child_medical_data_by_id(
    uow: UOWDep, child_medical_data_id: PositiveInt = Path(default=..., ge=1)
) -> ChildMedicalDataDetail:
    """
    Get child medical data by ID
    :param child_medical_data_id:
    :param uow:
    :return:
    """
    try:
        child_medical_data = (
            await ChildMedicalDataService().get_child_medical_data(
                uow=uow, id=child_medical_data_id
            )
        )
        return child_medical_data
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Child medical data not found",
        )


@router.put(
    path="/{child_medical_data_id}/",
    status_code=status.HTTP_200_OK,
    response_model=ChildMedicalDataDetail,
    name="Update child medical data by ID",
)
async def update_child_medical_data_by_id(
    uow: UOWDep,
    update_form: ChildMedicalDataUpdateForm,
    child_medical_data_id: PositiveInt = Path(default=..., ge=1),
) -> ChildMedicalDataDetail:
    """
    Update child data by ID
    :param uow:
    :param update_form:
    :param child_medical_data_id:
    :return:
    """
    try:
        update_child_medical_data = (
            await ChildMedicalDataService().update_child_medical_data(
                uow=uow, child=update_form, id=child_medical_data_id
            )
        )
        return update_child_medical_data
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Child medical data not found",
        )


@router.delete(
    path="/{child_medical_data_id}/",
    status_code=status.HTTP_200_OK,
    name="Delete child medical data by ID",
)
async def delete_child_medical_data_by_id(
    uow: UOWDep, child_medical_data_id: PositiveInt = Path(default=..., ge=1)
) -> dict:
    """
    Delete child medical data by ID
    :param uow:
    :param child_medical_data_id:
    :return:
    """
    try:
        await ChildMedicalDataService().delete_child_medical_data(
            uow=uow, id=child_medical_data_id
        )
        return {"msg": "Child medical data has been successfully removed"}
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Child medical data not found",
        )
