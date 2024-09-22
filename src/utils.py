from collections import Counter

import numpy as np

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.enums import ChildPulseRecoveryStatusEnum, ChildGenderEnum

from typing import Dict, Union
from datetime import datetime, date, timedelta

import jwt
from jwt import PyJWTError

from src.repositories.models import ChildRepository
from src.settings import SETTINGS


async def get_child(
    uow_children: ChildRepository, uow_session: AsyncSession, child_id: int
):
    """
    Get Child model
    :param uow_children:
    :param uow_session:
    :param child_id:
    :return:
    """
    stmt = select(uow_children.model).filter(uow_children.model.id == child_id)
    result = await uow_session.execute(stmt)
    return result.scalar_one()


async def create_access_token(sub: Union[str, int]) -> str:
    """
    Create access token
    :param sub:
    :return:
    """
    return jwt.encode(
        payload={
            "sub": str(sub),
            "exp": datetime.now()
            + timedelta(minutes=SETTINGS.ACCESS_TOKEN_EXPIRE),
        },
        key=str(SETTINGS.SECRET_KEY_OF_ACCESS_TOKEN),
        algorithm=SETTINGS.ALGORITHM,
    )


async def verify_access_token(access_token: str):
    """
    Verify access token
    :param access_token:
    :return:
    """
    try:
        payload = jwt.decode(
            access_token,
            key=str(SETTINGS.SECRET_KEY_OF_ACCESS_TOKEN),
            algorithms=[SETTINGS.ALGORITHM],
        )
    except PyJWTError:
        return None
    return payload


async def create_refresh_token(sub: Union[str, int]) -> str:
    """
    Create refresh token
    :param sub:
    :return:
    """
    return jwt.encode(
        payload={
            "sub": str(sub),
            "exp": datetime.now()
            + timedelta(minutes=SETTINGS.REFRESH_TOKEN_EXPIRE),
        },
        key=str(SETTINGS.SECRET_KEY_OF_REFRESH_TOKEN),
        algorithm=SETTINGS.ALGORITHM,
    )


async def verify_refresh_token(refresh_token: str):
    """
    Verify refresh token
    :param refresh_token:
    :return:
    """
    try:
        payload = jwt.decode(
            refresh_token,
            key=str(SETTINGS.SECRET_KEY_OF_REFRESH_TOKEN),
            algorithms=[SETTINGS.ALGORITHM],
        )
    except PyJWTError:
        return None
    return payload


async def get_pulse_recovery_status(
    lying_pulse: int, standing_pulse: int
) -> ChildPulseRecoveryStatusEnum:
    """
    Get pulse recovery status based on pulse measurements.
    """
    pulse_change = standing_pulse - lying_pulse

    if pulse_change < 0:
        return ChildPulseRecoveryStatusEnum.ERROR
    elif pulse_change <= 11:
        return ChildPulseRecoveryStatusEnum.GOOD
    elif 12 <= pulse_change <= 21:
        return ChildPulseRecoveryStatusEnum.AVERAGE
    else:
        return ChildPulseRecoveryStatusEnum.POOR


async def calculate_male_peek_age(
    current_age: float,
    standing_height: float,
    sitting_height: float,
    body_mass: float,
) -> float:
    """

    :param current_age:
    :param standing_height:
    :param sitting_height:
    :param body_mass:
    :return:
    """
    peak_age = current_age - (
        -9.236
        + (0.0002708 * ((standing_height - sitting_height) * sitting_height))
        + (-0.001663 * (current_age * (standing_height - sitting_height)))
        + (0.007216 * (current_age * sitting_height))
        + (0.02292 * ((body_mass / standing_height) * 100))
    )
    return peak_age


async def calculate_female_peek_age(
    current_age: float,
    standing_height: float,
    sitting_height: float,
    body_mass: float,
) -> float:
    """

    :param current_age:
    :param standing_height:
    :param sitting_height:
    :param body_mass:
    :return:
    """
    peak_age = current_age - (
        -9.376
        + (0.0001882 * ((standing_height - sitting_height) * sitting_height))
        + (0.0022 * (current_age * (standing_height - sitting_height)))
        + (0.005841 * (current_age * sitting_height))
        - (0.002658 * (current_age * body_mass))
        + (0.07693 * ((body_mass / standing_height) * 100))
    )
    return peak_age


async def all_male_ages(
    current_age: float, peak_age: float, gender: ChildGenderEnum
) -> Dict[str, float] | None:
    """
    Get all ages for males
    :param current_age:
    :param peak_age:
    :param gender:
    :return:
    """
    if peak_age:
        if gender == ChildGenderEnum.MALE:
            start_age = peak_age - 1
            end_age = peak_age + 2
        else:
            start_age = peak_age - 1.5
            end_age = peak_age + 2

        return {
            "current_age": round(current_age, 2),
            "start_age": round(start_age, 2),
            "peak_age": round(peak_age, 2),
            "end_age": round(end_age, 2),
        }
    else:
        return None


async def calculate_adolescence_info(
    birth_date: date,
    standing_height: float,
    sitting_height: float,
    body_mass: float,
    gender: str,
) -> Dict[str, float]:
    """
    Calculate adolescence information based on various metrics.
    """
    current_date = datetime.now().date()
    age_years = current_date.year - birth_date.year
    age_months = current_date.month - birth_date.month

    if age_months < 0:
        age_years -= 1
        age_months += 12

    current_age = age_years + age_months / 12

    if gender == ChildGenderEnum.MALE:
        male_peak_age = await calculate_male_peek_age(
            current_age=current_age,
            sitting_height=sitting_height,
            standing_height=standing_height,
            body_mass=body_mass,
        )
        all_ages = await all_male_ages(
            current_age=current_age, peak_age=male_peak_age, gender=gender
        )
        if all_ages:
            return all_ages
        else:
            return None
    elif gender == ChildGenderEnum.FEMALE:
        female_peak_age = await calculate_female_peek_age(
            current_age=current_age,
            sitting_height=sitting_height,
            standing_height=standing_height,
            body_mass=body_mass,
        )
        all_ages = await all_male_ages(
            current_age=current_age, peak_age=female_peak_age, gender=gender
        )
        if all_ages:
            return all_ages
        else:
            return None
    else:
        raise ValueError(f"Invalid gender: {gender}")


async def calculate_disease_frequency(
    diseases: list, start_date=None, end_date=None
):
    """
    Рассчитать частоту заболеваний за определённый период времени.
    """
    dates = [datetime.strptime(disease[1], "%Y-%m-%d") for disease in diseases]

    if start_date is None:
        start_date = min(dates)
    else:
        start_date = datetime.strptime(start_date, "%Y-%m-%d")

    if end_date is None:
        end_date = max(dates)
    else:
        end_date = datetime.strptime(end_date, "%Y-%m-%d")

    filtered_diseases = [
        disease[0]
        for disease in diseases
        if start_date <= datetime.strptime(disease[1], "%Y-%m-%d") <= end_date
    ]

    disease_frequency = Counter(filtered_diseases)

    return dict(disease_frequency)


async def get_season(
    date_data: datetime,
) -> str | dict[str, int]:
    """
    Определить сезон года по дате. Возвращает строку с названием сезона.
    """
    month = date_data.month
    if month in [12, 1, 2]:
        return "Зима"
    elif month in [3, 4, 5]:
        return "Весна"
    elif month in [6, 7, 8]:
        return "Лето"
    elif month in [9, 10, 11]:
        return "Осень"
    else:
        raise ValueError(f"Invalid date_data: {date_data}")


async def calculate_seasonal_trends(diseases: list):
    """
    Рассчитывается частота заболеваний по сезонам года.
    """

    if diseases:
        seasons = [
            await get_season(datetime.strptime(disease[1], "%Y-%m-%d"))
            for disease in diseases
        ]
        season_frequency = Counter(seasons)
        return dict(season_frequency)


async def calculate_rohrer_index(weight_kg: float, height_cm: float):
    """
    Рассчитывает индекс Рорера
    """
    weight_grams = weight_kg * 1000

    rohrer_index = (weight_grams / (height_cm**3)) * 10**7

    if rohrer_index < 1.2:
        interpretation = "Недостаточный вес"
    elif 1.2 <= rohrer_index <= 1.4:
        interpretation = "Норма"
    else:
        interpretation = "Избыточный вес"

    return rohrer_index, interpretation


async def calculate_height_weight_ratio(weight_kg: float, height_cm: float):
    """
    Рассчитывает соотношение веса к росту
    """

    ratio = weight_kg / height_cm

    return ratio


async def calculate_bsa(height_cm: float, weight_kg: float):
    """
    Рассчитывает площадь поверхности тела (BSA) на основе роста и веса
    """

    bsa = (
        0.007184 * (height_cm**0.725) * (weight_kg**0.425)
    )  # Формула для расчета BSA

    return bsa


async def calculate_ideal_body_weight(height_cm: float, age_year: int):
    """
    Рассчитывает идеальную массу тела в зависимости от роста и возраста
    """

    ideal_weight = height_cm - 100 - (age_year / 10 * 0.5)

    return ideal_weight


async def interpret_bmi(bmi: float, gender: ChildGenderEnum):
    """
    Интерпретирует ИМТ на основе возрастных и половых перцентильных таблиц.
    """

    if gender == ChildGenderEnum.FEMALE:
        if bmi < 16.0:
            return "Недостаточная масса тела"
        elif 16.0 <= bmi < 21.0:
            return "Нормальная масса тела"
        elif 21.0 <= bmi < 25.0:
            return "Избыточная масса тела"
        else:
            return "Ожирение"
    elif gender == ChildGenderEnum.MALE:
        if bmi < 16.0:
            return "Недостаточная масса тела"
        elif 16.0 <= bmi < 22.0:
            return "Нормальная масса тела"
        elif 22.0 <= bmi < 26.0:
            return "Избыточная масса тела"
        else:
            return "Ожирение"


async def calculate_bmi(weight_kg: float, height_m: float):
    """
    Рассчитывает индекс массы тела (ИМТ) на основе веса и роста.
    """

    bmi = weight_kg / (height_m**2)

    return bmi


async def calculate_subject_gpa(grades: list):
    """
    Вычисляет средний балл (GPA) по предметам на основе списка оценок.
    """

    if not grades:
        return None

    subject_gpa = sum(grades) / len(grades)

    return subject_gpa


async def get_quarter(month: int):
    """
    Определяет номер четверти на основе месяца в учебном году.
    """
    if month in [9, 10]:
        return "1"  # Первая четверть: сентябрь — октябрь
    elif month in [11, 12]:
        return "2"  # Вторая четверть: ноябрь — декабрь
    elif month in [1, 2, 3]:
        return "3"  # Третья четверть: январь — март
    elif month in [4, 5]:
        return "4"  # Четвертая четверть: апрель — май
    else:
        return "Летний период"


async def linear_regression_quarters(quarters: list, grades: list):
    """
    Выполняет линейную регрессию для анализа успеваемости по четвертям.
    """
    # Проверка на корректность входных данных
    if len(quarters) != len(grades) or len(quarters) == 0:
        return None

    # Преобразование данных в массивы NumPy
    x = np.array(quarters)
    y = np.array(grades)

    # Расчет коэффициентов линейной регрессии
    a = np.vstack([x, np.ones(len(x))]).T
    m, b = np.linalg.lstsq(a, y, rcond=None)[0]

    return m, b


async def analyze_performance(dates, grades):
    """
    Анализирует успеваемость на основе дат и оценок, используя линейную регрессию по четвертям.
    """
    if not dates or not grades:
        return None

    quarters = [await get_quarter(item_date) for item_date in dates]

    quarter_map = {"1": 1, "2": 2, "3": 3, "4": 4}
    numeric_quarters = [quarter_map[q] for q in quarters if q in quarter_map]

    if len(numeric_quarters) != len(grades):
        return None

    return await linear_regression_quarters(numeric_quarters, grades)


async def calculate_progress_ratio(
    current_avg_grade: int, previous_avg_grade: int
):
    """
    Вычисляет коэффициент прогресса для оценки изменения успеваемости.
    """
    if not current_avg_grade or not previous_avg_grade:
        return None

    progress_ratio = (current_avg_grade / previous_avg_grade) - 1
    return progress_ratio


async def calculate_pearson_correlation(x: list, y: list):
    """
    Вычисляет коэффициент корреляции Пирсона между двумя наборами данных.
    """
    if len(x) == 0 or len(y) == 0 or len(x) != len(y):
        return None

    # Преобразование в массивы
    x_array = np.array(x)
    y_array = np.array(y)

    # Вычисление средних значений
    x_mean = np.mean(x_array)
    y_mean = np.mean(y_array)

    # Вычисление числителя и знаменателя
    numerator = np.sum((x_array - x_mean) * (y_array - y_mean))
    denominator = np.sqrt(
        np.sum((x_array - x_mean) ** 2) * np.sum((y_array - y_mean) ** 2)
    )

    if denominator == 0:
        return None

    # Вычисление коэффициента корреляции
    r = numerator / denominator
    return r


async def predict_final_grade(grades: list):
    """
    Прогнозирует итоговую оценку на основе среднего значения имеющихся оценок.
    """

    # Проверка наличия данных
    if not grades:
        return None

    # Преобразование в массив NumPy для удобства расчетов
    grades_array = np.array(grades)

    # Вычисление среднего значения оценок
    predicted_grade = np.mean(grades_array)

    return predicted_grade
