from typing import Dict, Union
from datetime import datetime, date, timedelta

import jwt
from jwt import PyJWTError

from src.settings import pwd_context, SETTINGS


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


async def get_pulse_recovery_status(
    lying_pulse: int, standing_pulse: int
) -> Dict[str, str]:
    """
    Get pulse recovery status based on pulse measurements.
    """
    result = {}

    pulse_change = standing_pulse - lying_pulse

    if pulse_change < 0:
        result["pulse_change"] = (
            "Ошибка в замере: пульс в положении стоя не может быть меньше пульса в положении лёжа. Пожалуйста, перепроверьте замер и повторите запись."
        )
    elif pulse_change <= 11:
        result["pulse_change"] = "Хорошо"
    elif 12 <= pulse_change <= 21:
        result["pulse_change"] = "Средне"
    else:
        result["pulse_change"] = "Плохо"

    return result


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
    current_age: float, peak_age: float, gender: str
) -> Dict[str, float]:
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
