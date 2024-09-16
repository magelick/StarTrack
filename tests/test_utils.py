import datetime

import numpy
import pytest

from src.database.enums import ChildPulseRecoveryStatusEnum, ChildGenderEnum
from src.utils import (
    get_pulse_recovery_status,
    calculate_male_peek_age,
    calculate_female_peek_age,
    all_male_ages,
    calculate_adolescence_info,
    calculate_disease_frequency,
    get_season,
    calculate_seasonal_trends,
    calculate_rohrer_index,
    calculate_height_weight_ratio,
    calculate_bsa,
    calculate_ideal_body_weight,
    interpret_bmi,
    calculate_bmi,
    calculate_subject_gpa,
    get_quarter,
    linear_regression_quarters,
    predict_final_grade,
    analyze_performance,
    calculate_progress_ratio,
    calculate_pearson_correlation,
)
from contextlib import nullcontext as does_not_raise


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "lying_pulse, standing_pulse, expected_status, expectation",
    [
        (100, 110, ChildPulseRecoveryStatusEnum.GOOD, does_not_raise()),
        (100, 111, ChildPulseRecoveryStatusEnum.GOOD, does_not_raise()),
        (100, 112, ChildPulseRecoveryStatusEnum.AVERAGE, does_not_raise()),
        (100, 121, ChildPulseRecoveryStatusEnum.AVERAGE, does_not_raise()),
        (100, 130, ChildPulseRecoveryStatusEnum.POOR, does_not_raise()),
        (100, 90, ChildPulseRecoveryStatusEnum.ERROR, does_not_raise()),
        (
            100,
            "110",
            ChildPulseRecoveryStatusEnum.GOOD,
            pytest.raises(TypeError),
        ),
        (
            "100",
            112,
            ChildPulseRecoveryStatusEnum.AVERAGE,
            pytest.raises(TypeError),
        ),
    ],
)
async def test_get_pulse_recovery_status(
    lying_pulse, standing_pulse, expected_status, expectation
):
    """
    Test get_pulse_recovery_status function
    """
    with expectation:
        status = await get_pulse_recovery_status(lying_pulse, standing_pulse)

        assert status == expected_status


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "current_age, standing_height, sitting_height, body_mass, expectation",
    [
        (15.8, 176.4, 110.3, 65.1, does_not_raise()),
        ("15.8", 176.4, 110.3, 65.1, pytest.raises(TypeError)),
        (15.8, "176.4", 110.3, 65.1, pytest.raises(TypeError)),
        (15.8, 176.4, "110.3", 65.1, pytest.raises(TypeError)),
        (15.8, 176.4, 110.3, "65.1", pytest.raises(TypeError)),
    ],
)
async def test_calculate_male_peek_age(
    current_age, standing_height, sitting_height, body_mass, expectation
):
    """
    Test calculate_male_peek_age function
    :param current_age:
    :param standing_height:
    :param sitting_height:
    :param body_mass:
    :return:
    """
    with expectation:
        male_peek_age = await calculate_male_peek_age(
            current_age, standing_height, sitting_height, body_mass
        )

        assert type(male_peek_age) is float


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "current_age, standing_height, sitting_height, body_mass, expectation",
    [
        (12.8, 159.4, 100.3, 52.2, does_not_raise()),
        ("12.8", 159.4, 100.3, 52.2, pytest.raises(TypeError)),
        (12.8, "159.4", 100.3, 52.2, pytest.raises(TypeError)),
        (12.8, 159.4, "100.3", 52.2, pytest.raises(TypeError)),
        (12.8, 159.4, 100.3, "52.2", pytest.raises(TypeError)),
    ],
)
async def test_calculate_female_peek_age(
    current_age, standing_height, sitting_height, body_mass, expectation
):
    """
    Test calculate_female_peek_age function
    :param current_age:
    :param standing_height:
    :param sitting_height:
    :param body_mass:
    :return:
    """
    with expectation:
        female_peek_age = await calculate_female_peek_age(
            current_age, standing_height, sitting_height, body_mass
        )

        assert type(female_peek_age) is float


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "current_age, peak_age, gender, expectation",
    [
        (15.0, 18.0, ChildGenderEnum.MALE, does_not_raise()),
        (15.0, 18.0, ChildGenderEnum.FEMALE, does_not_raise()),
        (15.0, None, None, does_not_raise()),
        ("15.0", 18.0, ChildGenderEnum.MALE, pytest.raises(TypeError)),
        (15.0, "18.0", ChildGenderEnum.MALE, pytest.raises(TypeError)),
        ("15.0", 18.0, ChildGenderEnum.FEMALE, pytest.raises(TypeError)),
        (15.0, "18.0", ChildGenderEnum.FEMALE, pytest.raises(TypeError)),
    ],
)
async def test_all_male_ages(current_age, peak_age, gender, expectation):
    """
    Test all_male_ages function
    :param current_age:
    :param peak_age:
    :param gender:
    :return:
    """
    with expectation:
        age_info = await all_male_ages(current_age, peak_age, gender)

        if age_info is not None:
            assert type(age_info.get("current_age")) is float
            assert type(age_info.get("start_age")) is float
            assert type(age_info.get("peak_age")) is float
            assert type(age_info.get("end_age")) is float
        else:
            assert age_info is None


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "birth_date, standing_height, sitting_height, body_mass, gender, expectation",
    [
        (
            datetime.date(2000, 1, 1),
            176.4,
            110.3,
            65.1,
            ChildGenderEnum.MALE,
            does_not_raise(),
        ),
        (
            datetime.date(2000, 1, 1),
            "176.4",
            110.3,
            65.1,
            ChildGenderEnum.MALE,
            pytest.raises(TypeError),
        ),
        (
            datetime.date(2000, 1, 1),
            176.4,
            "110.3",
            65.1,
            ChildGenderEnum.MALE,
            pytest.raises(TypeError),
        ),
        (
            datetime.date(2000, 1, 1),
            176.4,
            110.3,
            "65.1",
            ChildGenderEnum.MALE,
            pytest.raises(TypeError),
        ),
        (
            1,
            176.4,
            110.3,
            65.1,
            ChildGenderEnum.MALE,
            pytest.raises(AttributeError),
        ),
        (
            datetime.date(2000, 1, 1),
            159.4,
            100.3,
            52.2,
            ChildGenderEnum.FEMALE,
            does_not_raise(),
        ),
        (
            datetime.date(2000, 1, 1),
            "159.4",
            100.3,
            52.2,
            ChildGenderEnum.FEMALE,
            pytest.raises(TypeError),
        ),
        (
            datetime.date(2000, 1, 1),
            159.4,
            "100.3",
            52.2,
            ChildGenderEnum.FEMALE,
            pytest.raises(TypeError),
        ),
        (
            datetime.date(2000, 1, 1),
            159.4,
            100.3,
            "52.2",
            ChildGenderEnum.FEMALE,
            pytest.raises(TypeError),
        ),
        (
            datetime.date(2000, 1, 1),
            159.4,
            100.3,
            52.2,
            ChildGenderEnum.FEMALE,
            does_not_raise(),
        ),
        (
            1,
            159.4,
            100.3,
            52.2,
            ChildGenderEnum.FEMALE,
            pytest.raises(AttributeError),
        ),
        (
            datetime.date(2000, 1, 1),
            176.4,
            110.3,
            65.1,
            "Some Male",
            pytest.raises(ValueError),
        ),
        (
            datetime.date(2000, 1, 1),
            159.4,
            100.3,
            52.2,
            "Some Female",
            pytest.raises(ValueError),
        ),
    ],
)
async def test_calculate_adolescence_info(
    birth_date, standing_height, sitting_height, body_mass, gender, expectation
):
    """
    Test calculate_adolescence_info function
    :param birth_date:
    :param standing_height:
    :param sitting_height:
    :param body_mass:
    :param gender:
    :param expectation:
    :return:
    """
    with expectation:
        adolescence_info = await calculate_adolescence_info(
            birth_date, standing_height, sitting_height, body_mass, gender
        )

        if adolescence_info is not None:
            assert type(adolescence_info.get("current_age")) is float
            assert type(adolescence_info.get("start_age")) is float
            assert type(adolescence_info.get("peak_age")) is float
            assert type(adolescence_info.get("end_age")) is float
        else:
            assert adolescence_info is None


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "diseases, start_date, end_date, expectation",
    [
        (
            [
                ("Disease1", "2022-01-01"),
                ("Disease2", "2022-01-15"),
                ("Disease1", "2022-01-20"),
            ],
            "2022-01-01",
            "2022-01-31",
            does_not_raise(),
        ),
        (
            [
                ("Disease1", "2022-01-01"),
                ("Disease2", "2022-01-15"),
                ("Disease1", "2022-01-20"),
            ],
            None,
            "2022-01-31",
            does_not_raise(),
        ),
        (
            [
                ("Disease1", "2022-01-01"),
                ("Disease2", "2022-01-15"),
                ("Disease1", "2022-01-20"),
            ],
            "2022-01-01",
            None,
            does_not_raise(),
        ),
        (
            [
                ("Disease1", "2022-01-01"),
                ("Disease2", "2022-01-15"),
                ("Disease1", "2022-01-20"),
            ],
            1,
            "2022-01-31",
            pytest.raises(TypeError),
        ),
        (
            [
                ("Disease1", "2022-01-01"),
                ("Disease2", "2022-01-15"),
                ("Disease1", "2022-01-20"),
            ],
            "2022-01-01",
            1,
            pytest.raises(TypeError),
        ),
    ],
)
async def test_calculate_disease_frequency(
    diseases, start_date, end_date, expectation
):
    """
    Test calculate_disease_frequency function
    :param diseases:
    :param start_date:
    :param end_date:
    :param expectation:
    :return:
    """
    with expectation:
        disease_frequency = await calculate_disease_frequency(
            diseases, start_date, end_date
        )

        assert type(disease_frequency) is dict

        for keys, values in disease_frequency.items():
            assert type(keys) is str
            assert type(values) is int


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "date_data, expectation",
    [
        (datetime.datetime(2000, 1, 1), does_not_raise()),
        (datetime.datetime(2000, 4, 1), does_not_raise()),
        (datetime.datetime(2000, 7, 1), does_not_raise()),
        (datetime.datetime(2000, 11, 1), does_not_raise()),
        (1, pytest.raises(AttributeError)),
    ],
)
async def test_get_season(date_data, expectation):
    """
    Test get_season function
    :param date_data:
    :param expectation:
    :return:
    """
    with expectation:
        season = await get_season(date_data)

        assert type(season) is str

        if date_data.month in [12, 1, 2]:
            assert season == "Зима"
        elif date_data.month in [3, 4, 5]:
            assert season == "Весна"
        elif date_data.month in [6, 7, 8]:
            assert season == "Лето"
        elif date_data.month in [9, 10, 11]:
            assert season == "Осень"


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "diseases, expectation",
    [
        (
            [
                ("Disease1", "2022-01-01"),
                ("Disease2", "2022-01-15"),
                ("Disease1", "2022-01-20"),
            ],
            does_not_raise(),
        ),
        ([], does_not_raise()),
    ],
)
async def test_calculate_seasonal_trends(diseases, expectation):
    """
    Test calculate_seasonal_trends function
    :param diseases:
    :return:
    """
    with expectation:
        seasonal_trends = await calculate_seasonal_trends(diseases)

        if seasonal_trends is not None:
            assert type(seasonal_trends) is dict

            for keys, values in seasonal_trends.items():
                assert type(keys) is str
                assert type(values) is int
        else:
            assert seasonal_trends is None


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "weight_kg, height_cm, expectation",
    [
        (60.0, 190.0, does_not_raise()),
        ("60.0", 190.0, pytest.raises(TypeError)),
        (60.0, "190.0", pytest.raises(TypeError)),
    ],
)
async def test_calculate_rohrer_index(weight_kg, height_cm, expectation):
    """
    Test calculate_rohrer_index function
    :param weight_kg:
    :param height_cm:
    :param expectation:
    :return:
    """
    with expectation:
        index_info = await calculate_rohrer_index(weight_kg, height_cm)

        rohrer_index, interpretation = index_info
        assert type(rohrer_index) is float
        assert type(interpretation) is str

        if rohrer_index < 1.2:
            assert interpretation == "Недостаточный вес"
        elif 1.2 <= rohrer_index <= 1.4:
            assert interpretation == "Норма"
        else:
            assert interpretation == "Избыточный вес"


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "weight_kg, height_cm, expectation",
    [
        (60.0, 190.0, does_not_raise()),
        ("60.0", 190.0, pytest.raises(TypeError)),
        (60.0, "190.0", pytest.raises(TypeError)),
    ],
)
async def test_calculate_height_weight_ratio(
    weight_kg, height_cm, expectation
):
    """
    Test calculate_height_weight_ratio function
    :param weight_kg:
    :param height_cm:
    :param expectation:
    :return:
    """
    with expectation:
        ratio = await calculate_height_weight_ratio(weight_kg, height_cm)
        assert type(ratio) is float


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "weight_kg, height_cm, expectation",
    [
        (60.0, 190.0, does_not_raise()),
        ("60.0", 190.0, pytest.raises(TypeError)),
        (60.0, "190.0", pytest.raises(TypeError)),
    ],
)
async def test_calculate_bsa(weight_kg, height_cm, expectation):
    """
    Test calculate_bsa
    :param weight_kg:
    :param height_cm:
    :param expectation:
    :return:
    """
    with expectation:
        bsa = await calculate_bsa(weight_kg, height_cm)
        assert type(bsa) is float


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "height_cm, age_year, expectation",
    [
        (180.0, datetime.date(2000, 1, 1).year, does_not_raise()),
        ("180.0", datetime.date(2000, 1, 1).year, pytest.raises(TypeError)),
    ],
)
async def test_calculate_ideal_body_weight(height_cm, age_year, expectation):
    """
    Test calculate_ideal_body_weight function
    :param height_cm:
    :param age_year:
    :param expectation:
    :return:
    """
    with expectation:
        ideal_weight = await calculate_ideal_body_weight(height_cm, age_year)

        assert type(ideal_weight) is float


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "bmi, gender, expectation",
    [
        (13.0, ChildGenderEnum.MALE, does_not_raise()),
        (18.0, ChildGenderEnum.MALE, does_not_raise()),
        (24.0, ChildGenderEnum.MALE, does_not_raise()),
        (27.0, ChildGenderEnum.MALE, does_not_raise()),
        (13.0, ChildGenderEnum.FEMALE, does_not_raise()),
        (18.0, ChildGenderEnum.FEMALE, does_not_raise()),
        (24.0, ChildGenderEnum.FEMALE, does_not_raise()),
        (27.0, ChildGenderEnum.FEMALE, does_not_raise()),
        ("13.0", ChildGenderEnum.MALE, pytest.raises(TypeError)),
        ("18.0", ChildGenderEnum.FEMALE, pytest.raises(TypeError)),
    ],
)
async def test_interpret_bmi(bmi, gender, expectation):
    """
    Test interpret_bmi function
    :param bmi:
    :param gender:
    :param expectation:
    :return:
    """
    with expectation:
        some_bmi = await interpret_bmi(bmi, gender)

        if gender == ChildGenderEnum.FEMALE:
            if bmi < 16:
                assert some_bmi == "Недостаточная масса тела"
            elif 16 <= bmi < 21:
                assert some_bmi == "Нормальная масса тела"
            elif 21 <= bmi < 25:
                assert some_bmi == "Избыточная масса тела"
            else:
                assert some_bmi == "Ожирение"
        elif gender == ChildGenderEnum.MALE:
            if bmi < 16:
                assert some_bmi == "Недостаточная масса тела"
            elif 16 <= bmi < 22:
                assert some_bmi == "Нормальная масса тела"
            elif 22 <= bmi < 26:
                assert some_bmi == "Избыточная масса тела"
            else:
                assert some_bmi == "Ожирение"


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "weight_kg, height_cm, expectation",
    [
        (60.0, 190.0, does_not_raise()),
        ("60.0", 190.0, pytest.raises(TypeError)),
        (60.0, "190.0", pytest.raises(TypeError)),
    ],
)
async def test_calculate_bmi(weight_kg, height_cm, expectation):
    """
    Test calculate_bmi function
    :param weight_kg:
    :param height_cm:
    :param expectation:
    :return:
    """
    with expectation:
        new_bmi = await calculate_bmi(weight_kg, height_cm)

        assert type(new_bmi) is float


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "grades, expectation",
    [
        ([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], does_not_raise()),
        ([], does_not_raise()),
    ],
)
async def test_calculate_subject_gpa(grades, expectation):
    """
    Test calculate_subject_gpa function
    :param grades:
    :param expectation:
    :return:
    """
    with expectation:
        subject_gpa = await calculate_subject_gpa(grades)

        if subject_gpa is not None:
            assert type(subject_gpa) is float
        else:
            assert subject_gpa is None


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "month, expectation",
    [
        (datetime.date(2000, 9, 1).month, does_not_raise()),
        (datetime.date(2000, 12, 1).month, does_not_raise()),
        (datetime.date(2000, 2, 1).month, does_not_raise()),
        (datetime.date(2000, 5, 1).month, does_not_raise()),
        (datetime.date(2000, 7, 1).month, does_not_raise()),
    ],
)
async def test_get_quarter(month, expectation):
    """
    Test get_quarter function
    :param month:
    :param expectation:
    :return:
    """
    with expectation:
        some_quarter = await get_quarter(month)

        assert type(some_quarter) is str

        if month in [9, 10]:
            assert some_quarter == "1"
        elif month in [11, 12]:
            assert some_quarter == "2"
        elif month in [1, 2, 3]:
            assert some_quarter == "3"
        elif month in [4, 5]:
            assert some_quarter == "4"
        else:
            assert some_quarter == "Летний период"


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "quarters, grades, expectation",
    [
        ([1, 2, 3, 4, 5], [1, 2, 3, 4, 5], does_not_raise()),
        ([], [1, 2, 3, 4, 5], does_not_raise()),
        ([1, 2, 3, 4, 5], [], does_not_raise()),
    ],
)
async def test_linear_regression_quarters(quarters, grades, expectation):
    """
    Test linear_regression_quarters function
    :param quarters:
    :param grades:
    :param expectation:
    :return:
    """
    with expectation:
        result = await linear_regression_quarters(quarters, grades)

        if result is not None:
            first_value, second_value = result

            assert type(first_value) is numpy.float64
            assert type(second_value) is numpy.float64
        else:
            assert result is None


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "dates, grades, expectation",
    [
        (
            [
                datetime.date(2000, 1, 1).month,
                datetime.date(2000, 4, 1).month,
                datetime.date(2000, 8, 1).month,
            ],
            [1, 2, 3, 4, 5],
            does_not_raise(),
        ),
        ([], [1, 2, 3, 4, 5], does_not_raise()),
        (
            [
                datetime.date(2000, 1, 1).month,
                datetime.date(2000, 4, 1).month,
                datetime.date(2000, 8, 1).month,
            ],
            [],
            does_not_raise(),
        ),
    ],
)
async def test_analyze_performance(dates, grades, expectation):
    """
    Test analyze_performance function
    :param dates:
    :param grades:
    :param expectation:
    :return:
    """
    with expectation:
        result = await analyze_performance(dates, grades)

        if result is not None:
            first_value, second_value = result

            assert type(first_value) is numpy.float64
            assert type(second_value) is numpy.float64
        else:
            assert result is None


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "current_avg_grade, previous_avg_grade, expectation",
    [
        (1, 2, does_not_raise()),
        ("1", 2, pytest.raises(TypeError)),
        (1, "2", pytest.raises(TypeError)),
    ],
)
async def test_calculate_progress_ratio(
    current_avg_grade, previous_avg_grade, expectation
):
    """
    Test calculate_progress_ratio function
    :param current_avg_grade:
    :param previous_avg_grade:
    :param expectation:
    :return:
    """
    with expectation:
        progress_ratio = await calculate_progress_ratio(
            current_avg_grade, previous_avg_grade
        )

        if progress_ratio is not None:
            assert type(progress_ratio) is float
        else:
            assert progress_ratio is None


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "x, y, expectation",
    [
        ([1, 2, 3, 4, 5], [1, 2, 3, 4, 5], does_not_raise()),
        ([], [1, 2, 3, 4, 5], does_not_raise()),
        ([1, 2, 3, 4, 5], [], does_not_raise()),
    ],
)
async def test_calculate_pearson_correlation(x, y, expectation):
    """
    Test calculate_pearson_correlation function
    :param x:
    :param y:
    :param expectation:
    :return:
    """
    with expectation:
        pearson_correlation = await calculate_pearson_correlation(x, y)

        if pearson_correlation is not None:
            assert type(pearson_correlation) is numpy.float64
        else:
            assert pearson_correlation is None


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "grades, expectation",
    [
        ([1, 2, 3, 4, 5], does_not_raise()),
        ([], does_not_raise()),
    ],
)
async def test_predict_final_grade(grades, expectation):
    """
    Test predict_final_grade function
    :param grades:
    :param expectation:
    :return:
    """
    with expectation:
        final_grade = await predict_final_grade(grades)

        if final_grade is not None:
            assert type(final_grade) is numpy.float64
        else:
            assert final_grade is None
