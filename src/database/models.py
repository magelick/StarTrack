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
    Integer,
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

class BloodType(Enum):
    """
    Enum class for Child Medical blood_type
    """

    A_POSITIVE = "A+"
    A_NEGATIVE = "A-"
    B_POSITIVE = "B+"
    B_NEGATIVE = "B-"
    AB_POSITIVE = "AB+"
    AB_NEGATIVE = "AB-"
    O_POSITIVE = "O+"
    O_NEGATIVE = "O-"


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

    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    date_of_birth = Column(Date, nullable=False)
    age = Column(Union[Float, SmallInteger], nullable=False)  # type: ignore
    gender = Column(SqlEnum(GenderEnum), nullable=False)  # type: ignore
    photo_url = Column(String(200), nullable=True)
    illness_history = Column(JSON, nullable=True)  # Child's illness history
    medical_diagnoses = Column(JSON, nullable=True)  # Child's medical diagnoses
    parents = relationship(
        "User", secondary=UserChild.__table__, back_populates="children"
    )

class ChildData(Base):
    """
    Child Data
    """

    date = Column(Date, nullable=False, default=datetime.now)  # Record date
    feedback = Column(String(200), nullable=True)  # Feedback from parents or guardians
    pulse_recovery_status = Column(String(100), nullable=True)  # Pulse recovery status
    adolescence_info = Column(String(200), nullable=True)  # Information about adolescence
    entry_type = Column(String, nullable=False)  # Record type (e.g., medical, psychological, etc.)
    child_id = Column(Integer, ForeignKey('child.id'), nullable=False)  # Child identifier
    child = relationship(
        'Child', back_populates='child_data'
    )

class ChildMedical(Base):
    """
    Child Medical
    """

    # Fields for medical data
    vaccinations = Column(JSON, nullable=True)  # Child's vaccinations, including dates and types
    medications_and_procedures = Column(JSON, nullable=True)  # Medications and medical procedures
    height = Column(Float, nullable=False)  # Child's height (possibly in "height" format)
    weight = Column(Float, nullable=False)  # Child's weight (possibly in "weight" format)
    blood_tests = Column(JSON, nullable=True)  # Results of blood tests
    urine_tests = Column(JSON, nullable=True)  # Results of urine tests
    other_tests = Column(JSON, nullable=True)  # Results of other medical tests (e.g., X-rays, MRIs)
    blood_type = Column(SqlEnum(BloodType), nullable=True)  # Blood type
    child = relationship(
        "Child", back_populates="child_medical"
    )

class ChildHealthStatus(Base):
    """
    Child Health Status
    """

    # Fields for current health status and activity
    current_symptoms = Column(JSON, nullable=True)  # Current symptoms or health issues
    frequency_of_illnesses = Column(JSON, nullable=True)  # Frequency of colds, allergies, or other illnesses
    doctor_visits = Column(JSON, nullable=True)  # History of doctor visits, including dates and reasons
    stress_anxiety_depression = Column(JSON, nullable=True)  # Frequency and causes of stress, anxiety, or depression
    emotional_state = Column(JSON, nullable=True)  # Overall emotional state (e.g., happiness, sadness)
    child = relationship(
        "Child", back_populates="child_health_status"
    )

class ChildDevelopment(Base):
    """
    Child Development
    """

    # Fields for development and interaction
    peer_interactions = Column(JSON, nullable=True)  # Interaction with peers
    communication_skills = Column(JSON, nullable=True)  # Communication and collaboration skills
    attention_level = Column(JSON, nullable=True)  # Attention level
    memory_level = Column(JSON, nullable=True)  # Memory level
    problem_solving_skills = Column(JSON, nullable=True)  # Problem-solving skills
    cognitive_tests = Column(JSON, nullable=True)  # Results of cognitive development tests
    emotional_tests = Column(JSON, nullable=True)  # Results of emotional development tests
    child = relationship(
        "Child", back_populates="child_development"
    )

class ChildPhysicalActivity(Base):
    """
    Child Physical Activity
    """

    # Fields for physical activity and health
    physical_exercises = Column(JSON, nullable=True)  # Frequency and type of physical exercises or sports activities
    daily_activity_level = Column(JSON, nullable=True)  # Activity level throughout the day
    coordination_and_flexibility = Column(JSON, nullable=True)  # Coordination and flexibility assessment
    injuries_and_chronic_pains = Column(JSON, nullable=True)  # Presence of injuries or chronic pains
    sports_achievements_and_interests = Column(JSON, nullable=True)  # Sports achievements and interests
    child = relationship(
        "Child", back_populates="child_physical_activity"
    )

class ChildAcademicData(Base):
    """
    Child Academic Data
    """

    # Fields for academic data
    academic_performance = Column(JSON, nullable=True)  # Grades and performance in subjects
    academic_achievements = Column(JSON, nullable=True)  # Achievements and successes in academics
    ework_time = Column(JSON, nullable=True)  # Time spent on homework
    attitude_towards_study = Column(JSON, nullable=True)  # Attitude towards studying and assignments
    areas_of_difficulty = Column(JSON, nullable=True)  # Specific difficulties in certain areas
    additional_support_needs = Column(JSON, nullable=True)  # Needs for additional support
    subject_interest = Column(JSON, nullable=True)  # Interest in subjects
    child = relationship(
        "Child", back_populates="child_academic_data"
    )

class ChildFamilyData(Base):
    """
    Child Family Data
    """

    # Fields for family information and parenting methods
    family_info = Column(JSON, nullable=True)  # Information about family and relatives
    family_involvement = Column(JSON, nullable=True)  # Family involvement in the child's life
    parenting_methods = Column(JSON, nullable=True)  # Parenting methods and their effectiveness
    behavior_and_discipline = Column(JSON, nullable=True)  # Behavior and discipline practices
    parental_attention_and_care = Column(JSON, nullable=True)  # Level of parental attention and care
    child = relationship(
        "Child", back_populates="child_family_data"
    )

class ChildNutritionData(Base):
    """
    Child Nutrition Data
    """

    # Fields for nutrition information
    dietary_info = Column(JSON, nullable=True)  # Dietary information
    snacking_habits = Column(JSON, nullable=True)  # Snacking habits
    beverage_consumption = Column(JSON, nullable=True)  # Beverage consumption
    supplements_and_vitamins = Column(JSON, nullable=True)  # Prescribed supplements and vitamins
    reactions_to_food = Column(JSON, nullable=True)  # Reactions to specific foods
    allergies_and_intolerances = Column(JSON, nullable=True)  # Information about allergies or intolerances
    child = relationship(
        "Child", back_populates="child_nutrition_data"
    )

