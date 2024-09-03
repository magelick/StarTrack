from typing import Dict
from datetime import datetime

# def get_children_for_user(session: Session, user_id: int) -> List[Type[Child]]:
#     """
#     Get all children related to a user.
#     """
#     return (
#         session.query(Child)
#         .join(UserChild)
#         .filter(UserChild.user_id == user_id)
#         .all()
#     )

# def get_users_for_child(session: Session, child_id: int) -> List[Type[User]]:
#     """
#     Get all users related to a child.
#     """
#     return (
#         session.query(User)
#         .join(UserChild)
#         .filter(UserChild.child_id == child_id)
#         .all()
#     )

# def is_user_child_relation_exists(session: Session, user_id: int, child_id: int) -> bool:
#     """
#     Check if a relation between a user and a child exists.
#     """
#     return session.query(UserChild).filter_by(user_id=user_id, child_id=child_id).first() is not None


# def get_user_by_id(session: Session, user_id: int) -> Optional[User]:
#     """
#     Get a user by ID.
#     """
#     return session.query(User).filter_by(id=user_id).first()
#
# def get_user_by_email(session: Session, email: str) -> Optional[User]:
#     """
#     Get a user by email.
#     """
#     return session.query(User).filter_by(email=email).first()


# def set_user_active_status(session: Session, user_id: int, is_active: bool) -> Optional[User]:
#     """
#     Set user's active status.
#     """
#     user = session.query(User).filter_by(id=user_id).first()
#     if user:
#         user.is_active = is_active
#         session.commit()
#     return user

# def update_user_password(session: Session, user_id: int, new_password: str) -> Optional[User]:
#     """
#     Update user's password with hashed value.
#     """
#     user = session.query(User).filter_by(id=user_id).first()
#     if user:
#         user.password = generate_password_hash(new_password)
#         session.commit()
#     return user

# def accept_terms(session: Session, user_id: int) -> Optional[User]:
#     """
#     Mark terms as accepted for the user.
#     """
#     user = session.query(User).filter_by(id=user_id).first()
#     if user:
#         user.terms_accepted = True
#         session.commit()
#     return user


async def get_pulse_recovery_status(lying_pulse: int, standing_pulse: int) -> Dict[str, str]:
    """
    Get pulse recovery status based on pulse measurements.
    """
    # Использовать Enum
    result = {}

    pulse_change = standing_pulse - lying_pulse

    if pulse_change < 0:
        result['pulse_change'] = "Ошибка в замере: пульс в положении стоя не может быть меньше пульса в положении лёжа. Пожалуйста, перепроверьте замер и повторите запись."
    elif pulse_change <= 11:
        result['pulse_change'] = "Хорошо"
    elif 12 <= pulse_change <= 21:
        result['pulse_change'] = "Средне"
    else:
        result['pulse_change'] = "Плохо"

    return result


async def calculate_male_peek_age(current_age: float, standing_height: float, sitting_height: float, body_mass: float) -> float:
    """

    :param standing_height:
    :param sitting_height:
    :param body_mass:
    :return:
    """
    peak_age = (current_age - (-9.236 + (0.0002708 * ((standing_height - sitting_height) * sitting_height))
                               + (-0.001663 * (current_age * (standing_height - sitting_height)))
                               + (0.007216 * (current_age * sitting_height))
                               + (0.02292 * ((body_mass / standing_height) * 100))))
    return peak_age


async def calculate_female_peek_age(current_age: float, standing_height: float, sitting_height: float,
                                  body_mass: float) -> float:
    """

    :param standing_height:
    :param sitting_height:
    :param body_mass:
    :return:
    """
    peak_age = (current_age - (-9.376 + (0.0001882 * ((standing_height - sitting_height) * sitting_height))
                                   + (0.0022 * (current_age * (standing_height - sitting_height)))
                                   + (0.005841 * (current_age * sitting_height))
                                   - (0.002658 * (current_age * body_mass))
                                   + (0.07693 * ((body_mass / standing_height) * 100))))
    return peak_age


async def all_male_ages(current_age: float, peak_age: float, gender: str) -> Dict[str, float]:
    """

    :param current_age:
    :param peak_age:
    :param gender:
    :return:
    """
    if gender == 'male':
        start_age = peak_age - 1
        end_age = peak_age + 2
    else:
        start_age = peak_age - 1.5
        end_age = peak_age + 2

    return {
        'current_age': round(current_age, 2),
        'start_age': round(start_age, 2),
        'peak_age': round(peak_age, 2),
        'end_age': round(end_age, 2)
    }


async def calculate_adolescence_info(birth_date: datetime.date, standing_height: float, sitting_height: float, body_mass: float, gender: str) -> Dict[str, float]:
    """
    Calculate adolescence information based on various metrics.
    """
    current_date = datetime.now()
    age_years = current_date.year - birth_date.year
    age_months = current_date.month - birth_date.month

    if age_months < 0:
        age_years -= 1
        age_months += 12

    current_age = age_years + age_months / 12

    if gender == 'male':
        male_peak_age = await calculate_male_peek_age(current_age=current_age, sitting_height=sitting_height, standing_height=standing_height, body_mass=body_mass)
        all_ages = await all_male_ages(current_age=current_age, peak_age=male_peak_age, gender=gender)
        return all_ages
    else:
        female_peak_age = await calculate_female_peek_age(current_age=current_age, sitting_height=sitting_height, standing_height=standing_height, body_mass=body_mass)
        all_ages = await all_male_ages(current_age=current_age, peak_age=female_peak_age, gender=gender)
        return all_ages

