from typing import Union

from sqlalchemy import (
    Column,
    String,
    DateTime,
    Boolean,
    Date,
    ForeignKey,
    Enum as SqlEnum,
    SmallInteger,
    Float,
)
from sqlalchemy.orm import relationship
from datetime import datetime
from enum import Enum

from src.database.base import Base


class UserRoleEnum(Enum):
    """
    Enum class for User role
    """

    PARENT = "parent"
    COACH = "coach"


class GenderEnum(Enum):
    """
    Enum class for Child gender
    """

    MALE = "Male"
    FEMALE = "Female"


class SportTypeEnum(Enum):
    """
    Enum class for Coach sport_type
    """

    SOCCER = "Football"
    BASKETBALL = "Basketball"
    HOCKEY = "Hockey"
    VOLLEYBALL = "Volleyball"
    TENNIS = "Tennis"
    SWIMMING = "Swimming"
    ATHLETICS = "Athletics"
    BOXING = "Boxing"
    GYMNASTICS = "Gymnastics"
    FENCING = "Fencing"
    FIGURE_SKATING = "Figure Skating"
    OTHER = "Other"


class UserChild(Base):
    """
    Intermediate model between User and Child
    """

    user_id = Column(
        SmallInteger,
        ForeignKey(column="user.id", ondelete="NO ACTION"),
        primary_key=True,
        nullable=False,
    )
    child_id = Column(
        SmallInteger,
        ForeignKey(column="child.id", ondelete="NO ACTION"),
        primary_key=True,
        nullable=False,
    )


class User(Base):
    """
    User model
    """

    first_name = Column(String(100), nullable=True)
    last_name = Column(String(100), nullable=True)
    email = Column(String(128), unique=True, nullable=False)
    password = Column(String(128), nullable=False)
    role = Column(SqlEnum(UserRoleEnum), nullable=False)  # type: ignore
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, onupdate=datetime.now)
    is_active = Column(Boolean, default=True)
    terms_accepted = Column(Boolean, default=False)
    children = relationship(
        argument="Child",
        secondary=UserChild.__table__,
        back_populates="parents",
    )


class Child(Base):
    """
    Child Model
    """

    first_name = Column(String(100), nullable=True)
    last_name = Column(String(100), nullable=True)
    date_of_birth = Column(Date, nullable=False)
    age = Column(Union[Float, SmallInteger], nullable=False)  # type: ignore
    gender = Column(SqlEnum(GenderEnum), nullable=False)  # type: ignore
    photo_url = Column(String(200), nullable=True)
    parents = relationship(
        "User", secondary=UserChild.__table__, back_populates="children"
    )
