from typing import List
from fastapi import APIRouter, Path
from fastapi.responses import ORJSONResponse
from pydantic import PositiveInt
from starlette import status


from src.schemas.child import ChildDetail, ChildAddForm, ChildUpdateForm
from src.services.child import ChildService
from src.dependencies import UOWDep

# Initial child router
router = APIRouter(
    prefix="/child", tags=["Child"], default_response_class=ORJSONResponse
)


@router.get(
    path="",
    status_code=status.HTTP_200_OK,
    response_model=List[ChildDetail],
    name="Get list of children",
)
async def get_list_children(uow: UOWDep) -> List[ChildDetail]:
    """
    Get list of children
    :param uow:
    :return:
    """
    users = await ChildService().get_children(uow=uow)
    return users


@router.post(
    path="",
    status_code=status.HTTP_201_CREATED,
    response_model=ChildDetail,
    name="Add new child",
)
async def add_new_child(uow: UOWDep, add_form: ChildAddForm) -> ChildDetail:
    """
    Add new child
    :param uow:
    :param add_form:
    :return:
    """
    new_child = await ChildService().add_child(uow=uow, child=add_form)
    return new_child


@router.get(
    path="/{child_id}/",
    status_code=status.HTTP_200_OK,
    response_model=ChildDetail,
    name="Get child by ID",
)
async def get_child_by_id(
    uow: UOWDep, child_id: PositiveInt = Path(default=..., ge=1)
) -> ChildDetail:
    """
    Get child by ID
    :param child_id:
    :param uow:
    :return:
    """
    child = await ChildService().get_child(uow=uow, id=child_id)
    return child


@router.put(
    path="/{child_id}/",
    status_code=status.HTTP_200_OK,
    response_model=ChildDetail,
    name="Update child by ID",
)
async def update_child_by_id(
    uow: UOWDep,
    update_form: ChildUpdateForm,
    child_id: PositiveInt = Path(default=..., ge=1),
) -> ChildDetail:
    """
    Update child by ID
    :param uow:
    :param update_form:
    :param child_id:
    :return:
    """
    update_child = await ChildService().update_child(
        uow=uow, child=update_form, id=child_id
    )
    return update_child


@router.put(
    path="/{child_id}/",
    status_code=status.HTTP_200_OK,
    name="Delete child by ID",
)
async def delete_child_by_id(
    uow: UOWDep, child_id: PositiveInt = Path(default=..., ge=1)
) -> dict:
    """
    Delete child by ID
    :param uow:
    :param child_id:
    :return:
    """
    await ChildService().delete_child(uow=uow, id=child_id)
    return {"msg": "Child has been successfully removed"}
