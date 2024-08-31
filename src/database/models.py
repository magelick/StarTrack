from sqlalchemy import Column, Integer, String, DateTime, Boolean, Date, ForeignKey, Enum as SqlEnum, Table
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import relationship
from datetime import datetime
from enum import Enum

class Base(declarative_base):
    id = Column(Integer, primary_key=True)

    @declared_attr
    def __tablename__(cls) -> str:
        return ''.join(f'_{i.lower()}' if i.isupper() else i for i in cls.__name__).strip('_')

engine = create_async_engine("sqlite+aiosqlite:///sqlite.db", echo=True)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

class UserRole(Enum):
    PARENT = "parent"
    COACH = "coach"

class GenderEnum(Enum):
    MALE = "Male"
    FEMALE = "Female"

class SportTypeEnum(Enum):
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

user_child_association = Table(
    'user_child_association', Base.metadata,
    Column('user_id', Integer, ForeignKey('user.id')),
    Column('child_profile_id', Integer, ForeignKey('child_profile.id'))
)

class User(Base):
    first_name = Column(String(100), nullable=True)
    last_name = Column(String(100), nullable=True)
    email = Column(String(128), unique=True, nullable=False)
    password = Column(String(128), nullable=False)
    role = Column(SqlEnum(UserRole), nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, onupdate=datetime.now)
    is_active = Column(Boolean, default=True)
    terms_accepted = Column(Boolean, default=False)

    children = relationship('Child', back_populates='parent')

    child_profiles = relationship(
        'ChildProfile',
        secondary=user_child_association,
        back_populates='users'
    )

class Coach(User):
    sport_type = Column(SqlEnum(SportTypeEnum), nullable=False)

class ChildProfile(Base):
    name = Column(String(100), nullable=False)
    date_of_birth = Column(Date, nullable=False)
    gender = Column(SqlEnum(GenderEnum), nullable=False)
    parent_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    parent = relationship('User', back_populates='children')
    avatar_url = Column(String(200), nullable=True)
    current_owner_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    current_owner = relationship('User', backref='owned_children', foreign_keys=[current_owner_id])

    users = relationship(
        'User',
        secondary=user_child_association,
        back_populates='child_profiles'
    )