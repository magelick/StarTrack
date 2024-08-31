import enum
from datetime import datetime
from typing import Optional

from pydantic import Field, EmailStr, PositiveInt
from src.schemas.base import DTO
from src.schemas.custom_types import AlphaStr


class UserBasic(DTO):
    """
    Basic User schema
    """

    first_name: AlphaStr = Field(
        default=None,
        max_length=100,
        title="User First Name",
        description="First name current user",
    )
    last_name: AlphaStr = Field(
        default=None,
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
    password = PasswordStr = Field(
        default=...,
        max_length=128,
        title="User Password",
        description="Password current user",
    )
    role: enum.Enum = Field(
        default=..., title="User Role", description="Role current user"
    )


class UserDetail(UserBasic):
    """
    User detail schema
    """

    id: PositiveInt = Field(
        default=..., title="User ID", description="ID current user"
    )
    created_at: Optional[datetime] = Field(
        default=datetime.now,
        title="User Created Time",
    )
    updated_at: Optional[datetime] = Field(
        default=datetime.now,
        title="User Updated Time",
    )
    is_active: bool = Field(default=True, title="User Active Check")
    terms_accepted: bool = Field(default=False, title="User Terms Accepted")
