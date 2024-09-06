
from typing import Dict, List, Optional
from datetime import datetime
from collections import Counter
from StarTrack.src.database.enums import PulseRecoveryStatus, ChildGenderEnum

from typing import Dict, Union
from datetime import datetime, date, timedelta

import jwt
from jwt import PyJWTError

from src.settings import pwd_context, SETTINGS


async def get_pulse_recovery_status(lying_pulse: int, standing_pulse: int) -> Dict[str, str]:
    """
    Get pulse recovery status based on pulse measurements.
    """
    pulse_change = standing_pulse - lying_pulse

    if pulse_change < 0:
        return {'pulse_change': PulseRecoveryStatus.ERROR.value}
    elif pulse_change <= 11:
        return {'pulse_change': PulseRecoveryStatus.GOOD.value}
    elif 12 <= pulse_change <= 21:
        return {'pulse_change': PulseRecoveryStatus.AVERAGE.value}
    else:
        return {'pulse_change': PulseRecoveryStatus.POOR.value}


async def create_hash_password(password: str) -> str:
    """
    Create hash password
    :param password:
    :return:
    """
    return pwd_context.hash(password)


async def verify_password(password: str, hash_password: str) -> bool:
    """
    Verify password
    :param password:
    :param hash_password:
    :return:
    """
    return pwd_context.verify(secret=password, hash=hash_password)


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



async def all_male_ages(current_age: float, peak_age: float, gender: ChildGenderEnum) -> Dict[str, float]:
    """

    :param current_age:
    :param peak_age:
    :param gender:
    :return:
    """
    if gender == "male":
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

    if gender == "male":
        male_peak_age = await calculate_male_peek_age(
            current_age=current_age,
            sitting_height=sitting_height,
            standing_height=standing_height,
            body_mass=body_mass,
        )
        all_ages = await all_male_ages(
            current_age=current_age, peak_age=male_peak_age, gender=gender
        )
        return all_ages
    else:
        female_peak_age = await calculate_female_peek_age(
            current_age=current_age,
            sitting_height=sitting_height,
            standing_height=standing_height,
            body_mass=body_mass,
        )
        all_ages = await all_male_ages(
            current_age=current_age, peak_age=female_peak_age, gender=gender
        )
        return all_ages

async def calculate_disease_frequency(diseases, start_date=None, end_date=None):
    """
    Рассчитать частоту заболеваний за определённый период времени.
    """
    dates = [datetime.strptime(disease[1], '%Y-%m-%d') for disease in diseases]

    if start_date is None:
        start_date = min(dates)
    else:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')

    if end_date is None:
        end_date = max(dates)
    else:
        end_date = datetime.strptime(end_date, '%Y-%m-%d')

    filtered_diseases = [
        disease[0] for disease in diseases
        if start_date <= datetime.strptime(disease[1], '%Y-%m-%d') <= end_date
    ]

    disease_frequency = Counter(filtered_diseases)

    return dict(disease_frequency)

async def calculate_seasonal_trends(diseases):
    """
    Рассчитывается частота заболеваний по сезонам года.
    """


async def get_season(date: datetime, diseases: Optional[List] = None) -> str | dict[str, int]:
    """
    Определить сезон года по дате. Возвращает строку с названием сезона.
    """
    month = date.month
    if month in [12, 1, 2]:
        return 'Зима'
    elif month in [3, 4, 5]:
        return 'Весна'
    elif month in [6, 7, 8]:
        return 'Лето'
    elif month in [9, 10, 11]:
        return 'Осень'

    if diseases:
        seasons = [await get_season(datetime.strptime(disease[1], '%Y-%m-%d')) for disease in diseases]
        season_frequency = Counter(seasons)
        return dict(season_frequency)

async def calculate_rohrer_index(weight_kg, height_cm):
    """
    Рассчитывает индекс Рорера
    """
    weight_grams = weight_kg * 1000

    rohrer_index = (weight_grams / (height_cm ** 3)) * 10 ** 7

    if rohrer_index < 1.2:
        interpretation = "Недостаточный вес"
    elif 1.2 <= rohrer_index <= 1.4:
        interpretation = "Норма"
    else:
        interpretation = "Избыточный вес"

    return rohrer_index, interpretation


async def calculate_height_weight_ratio(weight_kg, height_cm):
    """
    Рассчитывает соотношение веса к росту
    """

    ratio = weight_kg / height_cm

    return ratio


async def calculate_bsa(height_cm, weight_kg):
    """
    Рассчитывает площадь поверхности тела (BSA) на основе роста и веса
    """

    bsa = 0.007184 * (height_cm ** 0.725) * (weight_kg ** 0.425)  # Формула для расчета BSA

    return bsa

async def calculate_ideal_body_weight(height_cm, age_years):
    """
    Рассчитывает идеальную массу тела в зависимости от роста и возраста
    """

    ideal_weight = height_cm - 100 - (age_years / 10 * 0.5)

    return ideal_weight


async def interpret_bmi(bmi, gender):
    """
    Интерпретирует ИМТ на основе возрастных и половых перцентильных таблиц.
    """

    interpretation = None

    if gender == "female":
        if bmi < 16:
            interpretation = "Недостаточная масса тела"
        elif 16 <= bmi < 21:
            interpretation = "Нормальная масса тела"
        elif 21 <= bmi < 25:
            interpretation = "Избыточная масса тела"
        else:
            interpretation = "Ожирение"
    elif gender == "male":
        if bmi < 16:
            interpretation = "Недостаточная масса тела"
        elif 16 <= bmi < 22:
            interpretation = "Нормальная масса тела"
        elif 22 <= bmi < 26:
            interpretation = "Избыточная масса тела"
        else:
            interpretation = "Ожирение"

    return interpretation


async def calculate_bmi(weight_kg, height_m):
    """
    Рассчитывает индекс массы тела (ИМТ) на основе веса и роста.
    """

    bmi = weight_kg / (height_m ** 2)  # Формула для расчета ИМТ

    return bmi


async def calculate_bmi_with_interpretation(weight_kg, height_m, age_years, gender):
    """
    Рассчитывает ИМТ и возвращает его интерпретацию на основе возраста и пола.
    """

    bmi = calculate_bmi(weight_kg, height_m)
    interpretation = interpret_bmi(bmi, age_years, gender)

    return bmi, interpretation


async def calculate_subject_gpa(grades):
    """
    Вычисляет средний балл (GPA) по предметам на основе списка оценок.
    """

    if not grades:
        return None

    subject_gpa = sum(grades) / len(grades)

    return subject_gpa

async def get_quarter(month):
    """
    Определяет номер четверти на основе месяца в учебном году.
    """
    if month in [9, 10]:
        return 1  # Первая четверть: сентябрь — октябрь
    elif month in [11, 12]:
        return 2  # Вторая четверть: ноябрь — декабрь
    elif month in [1, 2, 3]:
        return 3  # Третья четверть: январь — март
    elif month in [4, 5]:
        return 4  # Четвертая четверть: апрель — май
    else:
        return 'Летний период'

async def linear_regression_quarters(quarters, grades, np=None):
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
    A = np.vstack([x, np.ones(len(x))]).T
    m, b = np.linalg.lstsq(A, y, rcond=None)[0]

    return m, b

async def analyze_performance(dates, grades):
    """
    Анализирует успеваемость на основе дат и оценок, используя линейную регрессию по четвертям.
    """
    if not dates or not grades:
        return None

    quarters = [await get_quarter(date[0]) for date in dates]

    quarter_map = {1: 1, 2: 2, 3: 3, 4: 4}
    numeric_quarters = [quarter_map[q] for q in quarters if q in quarter_map]

    if len(numeric_quarters) != len(grades):
        return None

    return await linear_regression_quarters(numeric_quarters, grades)


async def calculate_progress_ratio(current_avg_grade, previous_avg_grade):
    """
    Вычисляет коэффициент прогресса для оценки изменения успеваемости.
    """

    progress_ratio = (current_avg_grade / previous_avg_grade) - 1
    return progress_ratio


async def calculate_pearson_correlation(x, y, np=None):
    """
    Вычисляет коэффициент корреляции Пирсона между двумя наборами данных.
    """

    if len(x) == 0 or len(y) == 0 or len(x) != len(y):
        return None

    # Преобразование в массивы
    x = np.array(x)
    y = np.array(y)

    # Вычисление средних значений
    x_mean = np.mean(x)
    y_mean = np.mean(y)

    # Вычисление числителя и знаменателя
    numerator = np.sum((x - x_mean) * (y - y_mean))
    denominator = np.sqrt(np.sum((x - x_mean) ** 2) * np.sum((y - y_mean) ** 2))

    if denominator == 0:
        return None

    # Вычисление коэффициента корреляции
    r = numerator / denominator
    return r


async def predict_final_grade(grades, np=None):
    """
    Прогнозирует итоговую оценку на основе среднего значения имеющихся оценок.
    """

    # Проверка наличия данных
    if not grades:
        return None

    # Преобразование в массив NumPy для удобства расчетов
    grades = np.array(grades)

    # Вычисление среднего значения оценок
    predicted_grade = np.mean(grades)

    return predicted_grade

