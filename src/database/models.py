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
    parents = relationship(
        "User", secondary=UserChild.__table__, back_populates="children"
    )

class DiaryEntry(Base):

    date = Column(Date, nullable=False, default=datetime.now)  # Дата записи
    feedback = Column(String(200), nullable=True)  # Обратная связь от родителей или опекунов
    pulse_recovery_status = Column(String(100), nullable=True)  # Статус восстановления пульса
    adolescence_info = Column(String(200), nullable=True)  # Информация о подростковом возрасте
    entry_type = Column(String, nullable=False)  # Тип записи (например, медицинская, психологическая и т.д.)
    child_id = Column(Integer, ForeignKey('child_profile.id'), nullable=False)  # Идентификатор ребенка

    # Поля для медицинских данных
    illness_history = Column(JSON, nullable=True)  # История заболеваний ребенка
    medical_diagnoses = Column(JSON, nullable=True)  # Медицинские диагнозы ребенка
    vaccinations = Column(JSON, nullable=True)  # Вакцинации ребенка, включая даты и типы
    medications_and_procedures = Column(JSON, nullable=True)  # Лекарства и медицинские процедуры
    height_and_weight = Column(Float, nullable=True)  # Рост и вес ребенка (возможно, в формате "рост, вес")
    medical_test_results = Column(JSON, nullable=True)  # Результаты медицинских анализов (кровь, моча и т.д.)
    blood_type = Column(String(10), nullable=True)  # Группа крови

    # Поля для текущего состояния и активности
    current_symptoms = Column(JSON, nullable=True)  # Текущие симптомы или проблемы со здоровьем
    frequency_of_illnesses = Column(JSON, nullable=True)  # Частота простуд, аллергий или других заболеваний
    doctor_visits = Column(JSON, nullable=True)  # История посещений врачей, включая дату и причины визитов
    stress_anxiety_depression = Column(JSON, nullable=True)  # Частота и причины стресса, тревожности или депрессии
    emotional_state = Column(JSON, nullable=True)  # Общее эмоциональное состояние (например, счастье, грусть)

    # Поля для развития и взаимодействия
    peer_interactions = Column(JSON, nullable=True)  # Взаимодействие с сверстниками
    communication_skills = Column(JSON, nullable=True)  # Способности к коммуникации и сотрудничеству
    attention_level = Column(JSON, nullable=True)  # Уровень внимания
    memory_level = Column(JSON, nullable=True)  # Уровень памяти
    problem_solving_skills = Column(JSON, nullable=True)  # Способности к решению задач
    cognitive_tests = Column(JSON, nullable=True)  # Результаты тестов на когнитивное развитие
    emotional_tests = Column(JSON, nullable=True)  # Результаты тестов на эмоциональное развитие

    # Поля для физической активности и здоровья
    physical_exercises = Column(JSON, nullable=True)  # Частота и тип физических упражнений или занятий спортом
    daily_activity_level = Column(JSON, nullable=True)  # Уровень активности в течение дня
    coordination_and_flexibility = Column(JSON, nullable=True)  # Оценка координации движений и физической гибкости
    injuries_and_chronic_pains = Column(JSON, nullable=True)  # Присутствие травм или хронических болей
    sports_achievements_and_interests = Column(JSON, nullable=True)  # Спортивные достижения и интересы

    # Поля для учебных данных
    academic_performance = Column(JSON, nullable=True)  # Оценки и успеваемость по предметам
    academic_achievements = Column(JSON, nullable=True)  # Достижения и успехи в учебе
    ework_time = Column(JSON, nullable=True)  # Время, проводимое на выполнение домашних заданий
    attitude_towards_study = Column(JSON, nullable=True)  # Отношение к учебе и заданиям
    areas_of_difficulty = Column(JSON, nullable=True)  # Особенности и трудности в определённых областях
    additional_support_needs = Column(JSON, nullable=True)  # Потребности в дополнительной поддержке

    # Поля для семейной информации и методов воспитания
    family_info = Column(JSON, nullable=True)  # Информация о семье и родственниках
    family_involvement = Column(JSON, nullable=True)  # Участие родителей и других членов семьи в жизни ребенка
    parenting_methods = Column(JSON, nullable=True)  # Применяемые методы воспитания и их эффективность
    behavior_and_discipline = Column(JSON, nullable=True)  # Установки на поведение и дисциплину
    parental_attention_and_care = Column(JSON, nullable=True)  # Уровень внимания и заботы со стороны родителей

    # Поля для информации о питании
    dietary_info = Column(JSON, nullable=True)  # Информация о питании
    snacking_habits = Column(JSON, nullable=True)  # Склонность к перекусам
    beverage_consumption = Column(JSON, nullable=True)  # Потребление напитков
    supplements_and_vitamins = Column(JSON, nullable=True)  # Назначенные добавки и витамины
    reactions_to_food = Column(JSON, nullable=True)  # Реакция на определённые продукты
    allergies_and_intolerances = Column(JSON, nullable=True)  # Информация о любых аллергиях или непереносимостях

    child = relationship(
        'ChildProfile', back_populates='diary_entries'
    )
