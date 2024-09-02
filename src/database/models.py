from sqlalchemy import (
    VARCHAR,
    DATETIME,
    BOOLEAN,
    DATE,
    ForeignKey,
    Enum as SQL_ENUM,
    SMALLINT,
    FLOAT,
    INT,
    TEXT,
)
from sqlalchemy.orm import relationship, mapped_column, Mapped
from datetime import datetime

from src.database.base import Base
from src.database.enums import (
    UserRoleEnum,
    UserSportTypeEnum,
    ChildGenderEnum,
    ChildBloodTypeEnum,
    ChildEmotionalStateEnum,
    ChildDevelopmentEnum,
    ChildCommunicationEnum,
    ChildTowardStudyEnum,
    ChildParentingMethodsEnum,
    ChildParentalAttentionEnum,
)


class UserChild(Base):
    """
    Intermediate model between User and Child
    """

    user_id: Mapped[int] = mapped_column(
        SMALLINT,
        ForeignKey(column="user.id", ondelete="NO ACTION"),
        primary_key=True,
        nullable=False,
    )
    child_id: Mapped[int] = mapped_column(
        SMALLINT,
        ForeignKey(column="child.id", ondelete="NO ACTION"),
        primary_key=True,
        nullable=False,
    )


class User(Base):
    """
    User model
    """

    first_name: Mapped[str] = mapped_column(VARCHAR(128), nullable=True)
    last_name: Mapped[str] = mapped_column(VARCHAR(128), nullable=True)
    email: Mapped[str] = mapped_column(
        VARCHAR(128), unique=True, nullable=False
    )
    password: Mapped[str] = mapped_column(VARCHAR(128), nullable=False)
    role: Mapped[UserRoleEnum] = mapped_column(SQL_ENUM(UserRoleEnum), nullable=False)  # type: ignore
    created_at: Mapped[datetime] = mapped_column(
        DATETIME, default=datetime.now
    )
    updated_at: Mapped[datetime] = mapped_column(
        DATETIME, onupdate=datetime.now
    )
    sport_type: Mapped[UserSportTypeEnum] = mapped_column(SQL_ENUM(UserSportTypeEnum), nullable=True)  # type: ignore
    is_active: Mapped[bool] = mapped_column(BOOLEAN, default=True)
    terms_accepted: Mapped[bool] = mapped_column(BOOLEAN, default=False)
    children: Mapped[list["Child"]] = relationship(
        argument="Child",
        secondary="user_child",
        back_populates="parents",
    )


class Child(Base):
    """
    Child Model
    """

    first_name: Mapped[str] = mapped_column(VARCHAR(128), nullable=False)
    last_name: Mapped[str] = mapped_column(VARCHAR(128), nullable=False)
    date_of_birth: Mapped[DATE] = mapped_column(DATE, nullable=False)
    age: Mapped[int] = mapped_column(INT, nullable=False)  # type: ignore
    gender: Mapped[ChildGenderEnum] = mapped_column(SQL_ENUM(ChildGenderEnum), nullable=False)  # type: ignore
    photo_url: Mapped[str] = mapped_column(VARCHAR(256), nullable=True)
    illness_history: Mapped[str] = mapped_column(
        VARCHAR(256), nullable=True
    )  # Child's illness history
    medical_diagnoses: Mapped[str] = mapped_column(
        VARCHAR(256), nullable=True
    )  # Child's medical diagnoses
    parents: Mapped[list["User"]] = relationship(
        argument="User", secondary="user_child", back_populates="children"
    )
    child_data: Mapped[list["ChildData"]] = relationship(
        argument="ChildData", back_populates="child"
    )
    child_medical_data: Mapped[list["ChildMedicalData"]] = relationship(
        argument="ChildMedicalData", back_populates="child"
    )
    child_health_data: Mapped[list["ChildHealthData"]] = relationship(
        argument="ChildHealthData", back_populates="child"
    )
    child_development_data: Mapped[list["ChildDevelopmentData"]] = (
        relationship(argument="ChildDevelopmentData", back_populates="child")
    )
    child_physical_data: Mapped[list["ChildPhysicalData"]] = relationship(
        argument="ChildPhysicalData", back_populates="child"
    )
    child_academic_data: Mapped[list["ChildAcademicData"]] = relationship(
        argument="ChildAcademicData", back_populates="child"
    )
    child_family_data: Mapped[list["ChildFamilyData"]] = relationship(
        argument="ChildFamilyData", back_populates="child"
    )
    child_nutrition_data: Mapped[list["ChildNutritionData"]] = relationship(
        argument="ChildNutritionData", back_populates="child"
    )


class ChildData(Base):
    """
    Child basic data model
    """

    date: Mapped[DATE] = mapped_column(
        DATE, nullable=False, default=datetime.now
    )  # Record date
    feedback: Mapped[str] = mapped_column(
        TEXT, nullable=True
    )  # Feedback from parents or guardians
    pulse_recovery_status: Mapped[str] = mapped_column(
        VARCHAR(128), nullable=True
    )  # Pulse recovery status
    adolescence_info: Mapped[str] = mapped_column(
        VARCHAR(256), nullable=True
    )  # Information about adolescence
    entry_type: Mapped[str] = mapped_column(
        VARCHAR(128), nullable=False
    )  # Record type (e.g., medical, psychological, etc.)
    child_id: Mapped[int] = mapped_column(
        SMALLINT,
        ForeignKey(column="child.id", ondelete="CASCADE"),
        nullable=False,
    )
    child: Mapped["Child"] = relationship(
        argument="Child", back_populates="child_data"
    )


class ChildMedicalData(Base):
    """
    Child medical data model
    """

    date: Mapped[DATE] = mapped_column(
        DATE, nullable=False, default=datetime.now
    )  # Record date
    vaccinations: Mapped[str] = mapped_column(
        VARCHAR(256), nullable=True
    )  # Child's vaccinations, including dates and types
    medications: Mapped[str] = mapped_column(VARCHAR(256), nullable=True)
    procedures: Mapped[str] = mapped_column(VARCHAR(256), nullable=True)
    height: Mapped[float] = mapped_column(
        FLOAT, nullable=False
    )  # Child's height (possibly in "height" format)
    weight: Mapped[float] = mapped_column(
        FLOAT, nullable=False
    )  # Child's weight (possibly in "weight" format)
    blood_tests: Mapped[int] = mapped_column(
        INT, nullable=True
    )  # Results of blood tests
    urine_tests: Mapped[int] = mapped_column(
        INT, nullable=True
    )  # Results of urine tests
    # other_tests = mapped_column(JSON, nullable=True)  # Results of other medical tests (e.g., X-rays, MRIs)
    blood_type: Mapped[ChildBloodTypeEnum] = mapped_column(SQL_ENUM(ChildBloodTypeEnum), nullable=True)  # type: ignore
    child_id: Mapped[int] = mapped_column(
        SMALLINT,
        ForeignKey(column="child.id", ondelete="CASCADE"),
        nullable=False,
    )
    child: Mapped["Child"] = relationship(
        argument="Child", back_populates="child_medical_data"
    )


class ChildHealthData(Base):
    """
    Child health status data model
    """

    date: Mapped[DATE] = mapped_column(
        DATE, nullable=False, default=datetime.now
    )  # Record date
    current_symptoms: Mapped[str] = mapped_column(
        VARCHAR(256), nullable=True
    )  # Current symptoms or health issues
    frequency_of_illnesses: Mapped[str] = mapped_column(
        VARCHAR(256), nullable=True
    )  # Frequency of colds, allergies, or other illnesses
    doctor_visits: Mapped[int] = mapped_column(
        INT, nullable=True
    )  # Count doctor visits
    stress_anxiety_depression: Mapped[str] = mapped_column(
        VARCHAR(256), nullable=True
    )  # Frequency and causes of stress, anxiety, or depression
    emotional_state: Mapped[ChildEmotionalStateEnum] = mapped_column(SQL_ENUM(ChildEmotionalStateEnum), nullable=True)  # type: ignore
    child_id: Mapped[int] = mapped_column(
        SMALLINT,
        ForeignKey(column="child.id", ondelete="CASCADE"),
        nullable=False,
    )
    child: Mapped["Child"] = relationship(
        argument="Child", back_populates="child_health_data"
    )


class ChildDevelopmentData(Base):
    """
    Child development data model
    """

    date: Mapped[DATE] = mapped_column(
        DATE, nullable=False, default=datetime.now
    )  # Record date
    peer_interactions: Mapped[ChildDevelopmentEnum] = mapped_column(
        SQL_ENUM(ChildDevelopmentEnum), nullable=True
    )  # Interaction with peers
    communication_skills: Mapped[ChildCommunicationEnum] = mapped_column(
        SQL_ENUM(ChildCommunicationEnum), nullable=True
    )  # Communication and collaboration skills
    attention_level: Mapped[ChildDevelopmentEnum] = mapped_column(
        SQL_ENUM(ChildDevelopmentEnum), nullable=True
    )  # Attention level
    memory_level: Mapped[ChildDevelopmentEnum] = mapped_column(
        SQL_ENUM(ChildDevelopmentEnum), nullable=True
    )  # Memory level
    problem_solving_skills: Mapped[ChildDevelopmentEnum] = mapped_column(
        SQL_ENUM(ChildDevelopmentEnum), nullable=True
    )  # Problem-solving skills
    cognitive_tests: Mapped[ChildDevelopmentEnum] = mapped_column(
        SQL_ENUM(ChildDevelopmentEnum), nullable=True
    )  # Results of cognitive development tests
    emotional_tests: Mapped[ChildDevelopmentEnum] = mapped_column(
        SQL_ENUM(ChildDevelopmentEnum), nullable=True
    )  # Results of emotional development tests
    child_id: Mapped[int] = mapped_column(
        SMALLINT,
        ForeignKey(column="child.id", ondelete="CASCADE"),
        nullable=False,
    )
    child: Mapped["Child"] = relationship(
        argument="Child", back_populates="child_development_data"
    )


class ChildPhysicalData(Base):
    """
    Child physical activity data model
    """

    date: Mapped[DATE] = mapped_column(
        DATE, nullable=False, default=datetime.now
    )  # Record date
    physical_type: Mapped[str] = mapped_column(
        VARCHAR(256), nullable=True
    )  # Type of sports activities
    daily_activity_level: Mapped[int] = mapped_column(
        INT, nullable=True
    )  # Activity level throughout the day
    flexibility: Mapped[str] = mapped_column(
        VARCHAR(128), nullable=True
    )  # Coordination assessment
    coordination: Mapped[str] = mapped_column(
        VARCHAR(128), nullable=True
    )  # Flexibility assessment
    injuries_and_chronic_pains: Mapped[str] = mapped_column(
        VARCHAR(256), nullable=True
    )  # Presence of injuries or chronic pains
    sports_achievements: Mapped[str] = mapped_column(
        VARCHAR(256), nullable=True
    )  # Sports achievements
    interests: Mapped[str] = mapped_column(
        VARCHAR(256), nullable=True
    )  # Interests
    child_id: Mapped[int] = mapped_column(
        SMALLINT,
        ForeignKey(column="child.id", ondelete="CASCADE"),
        nullable=False,
    )
    child: Mapped["Child"] = relationship(
        argument="Child", back_populates="child_physical_data"
    )


class ChildAcademicData(Base):
    """
    Child academic data model
    """

    date: Mapped[DATE] = mapped_column(
        DATE, nullable=False, default=datetime.now
    )  # Record date
    academic_performance: Mapped[float] = mapped_column(
        FLOAT, nullable=True
    )  # Grades and performance in subjects
    academic_achievements: Mapped[str] = mapped_column(
        VARCHAR(256), nullable=True
    )  # Achievements and successes in academics
    work_time: Mapped[int] = mapped_column(
        INT, nullable=True
    )  # Time spent on homework
    attitude_towards_study: Mapped[ChildTowardStudyEnum] = mapped_column(
        SQL_ENUM(ChildTowardStudyEnum), nullable=True
    )  # Attitude towards studying and assignments
    areas_of_difficulty: Mapped[str] = mapped_column(
        VARCHAR(256), nullable=True
    )  # Specific difficulties in certain areas
    additional_support_needs: Mapped[bool] = mapped_column(
        BOOLEAN, default=True, nullable=True
    )  # Needs for additional support
    subject_interest: Mapped[str] = mapped_column(
        VARCHAR(256), nullable=True
    )  # Interest in subjects
    child_id: Mapped[int] = mapped_column(
        SMALLINT,
        ForeignKey(column="child.id", ondelete="CASCADE"),
        nullable=False,
    )
    child: Mapped["Child"] = relationship(
        argument="Child", back_populates="child_academic_data"
    )


class ChildFamilyData(Base):
    """
    Child family data model
    """

    date: Mapped[DATE] = mapped_column(
        DATE, nullable=False, default=datetime.now
    )  # Record date
    family_info: Mapped[str] = mapped_column(
        VARCHAR(256), nullable=True
    )  # Information about family and relatives
    family_involvement: Mapped[str] = mapped_column(
        VARCHAR(128), nullable=True
    )  # Family involvement in the child's life
    parenting_methods: Mapped[ChildParentingMethodsEnum] = mapped_column(SQL_ENUM(ChildParentingMethodsEnum), nullable=True)  # type: ignore
    # behavior_and_discipline = mapped_column(JSON, nullable=True)  # Behavior and discipline practices
    parental_attention_and_care: Mapped[ChildParentalAttentionEnum] = mapped_column(SQL_ENUM(ChildParentalAttentionEnum), nullable=True)  # type: ignore
    child_id: Mapped[int] = mapped_column(
        SMALLINT,
        ForeignKey(column="child.id", ondelete="CASCADE"),
        nullable=False,
    )
    child: Mapped["Child"] = relationship(
        argument="Child", back_populates="child_family_data"
    )


class ChildNutritionData(Base):
    """
    Child nutrition data model
    """

    date: Mapped[DATE] = mapped_column(
        DATE, nullable=False, default=datetime.now
    )  # Record date
    dietary_info: Mapped[str] = mapped_column(
        VARCHAR(256), nullable=True
    )  # Dietary information
    snacking_habits: Mapped[bool] = mapped_column(
        BOOLEAN, default=True, nullable=True
    )  # Snacking habits
    beverage_consumption: Mapped[bool] = mapped_column(
        BOOLEAN, default=True, nullable=True
    )  # Beverage consumption
    supplements_or_vitamins: Mapped[str] = mapped_column(
        VARCHAR(256), nullable=True
    )  # Prescribed supplements and vitamins
    reactions_to_food: Mapped[str] = mapped_column(
        VARCHAR(256), nullable=True
    )  # Reactions to specific foods
    allergies_or_intolerances: Mapped[str] = mapped_column(
        VARCHAR(256), nullable=True
    )  # Information about allergies or intolerances
    child_id: Mapped[int] = mapped_column(
        SMALLINT,
        ForeignKey(column="child.id", ondelete="CASCADE"),
        nullable=False,
    )
    child = relationship(
        argument="Child", back_populates="child_nutrition_data"
    )
