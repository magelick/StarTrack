from datetime import datetime
from typing import Optional

from pydantic import Field, EmailStr, PositiveInt

from src.database.enums import UserRoleEnum, UserSportTypeEnum
from src.schemas.base import DTO


class UserBasic(DTO):
    """
    Basic User schema
    """

    first_name: Optional[str] = Field(
        default=...,
        max_length=100,
        title="User First Name",
        description="First name current user",
    )
    last_name: Optional[str] = Field(
        default=...,
        max_length=100,
        title="User Last Name",
        description="Last name current user",
    )
    email: EmailStr = Field(
        default=...,
        max_length=128,
        title="User Email",
        description="Email current user",
    )
    role: UserRoleEnum = Field(
        default=..., title="User Role", description="Role current user"
    )
    sport_type: Optional[UserSportTypeEnum] = Field(
        default=None, title="Sport Type", description="Sport Type current user"
    )


class UserRegisterForm(UserBasic):
    """
    User Register schema
    """

    first_name: Optional[str] = Field(
        default=...,
        max_length=100,
        title="User First Name",
        description="First name current user",
    )
    last_name: Optional[str] = Field(
        default=...,
        max_length=100,
        title="User Last Name",
        description="Last name current user",
    )
    email: EmailStr = Field(
        default=...,
        max_length=128,
        title="User Email",
        description="Email current user",
    )


class UserUpdateForm(UserBasic):
    """
    User Update form
    """

    ...


class UserDetail(UserBasic):
    """
    User detail schema
    """

    id: PositiveInt = Field(
        default=..., title="User ID", description="ID current user"
    )
    created_at: Optional[datetime] = Field(
        default_factory=datetime.now,
        title="User Created Time",
    )
    updated_at: Optional[datetime] = Field(
        default_factory=datetime.now,
        title="User Updated Time",
    )
    is_active: bool = Field(default=True, title="User Active Check")
    terms_accepted: bool = Field(default=False, title="User Terms Accepted")
