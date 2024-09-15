import datetime

import pytest

from src.database.enums import (
    ChildGenderEnum,
    ChildPulseRecoveryStatusEnum,
    ChildBloodTypeEnum,
    ChildEmotionalStateEnum,
    ChildDevelopmentEnum,
    ChildCommunicationEnum,
    ChildTowardStudyEnum,
    ChildParentingMethodsEnum,
    ChildBehaviorDisciplineEnum,
    ChildParentalAttentionEnum,
)


class TestChildRepository:
    """
    TestCase for ChildRepository
    """

    @pytest.mark.asyncio
    async def test_child_repository_add_one(self, get_child_repository):
        """
        Test ChildRepository add one function
        :param get_child_repository:
        :return:
        """
        data = {
            "first_name": "Vasya",
            "last_name": "Pupkin",
            "date_of_birth": datetime.datetime.strptime(
                "2001-01-01", "%Y-%m-%d"
            ).date(),
            "height": 50.0,
            "weight": 170.0,
            "gender": ChildGenderEnum.MALE,
            "photo_url": "https://example.com/photo.jpg",
            "illness_history": "Test illness history",
            "medical_diagnoses": "Test medical diagnoses",
        }
        child = await get_child_repository.add_one(data=data)

        assert child.first_name == "Vasya"
        assert child.last_name == "Pupkin"
        assert child.date_of_birth == datetime.date(2001, 1, 1)
        assert child.height == 50.0
        assert child.weight == 170.0
        assert child.gender == ChildGenderEnum.MALE
        assert child.photo_url == "https://example.com/photo.jpg"
        assert child.illness_history == "Test illness history"
        assert child.medical_diagnoses == "Test medical diagnoses"

    @pytest.mark.asyncio
    async def test_child_repository_get_all(self, get_child_repository):
        """
        Test ChildRepository get all function
        :param get_child_repository:
        :return:
        """
        second_data = {
            "id": 2,
            "first_name": "Ivan",
            "last_name": "Petrov",
            "date_of_birth": datetime.datetime.strptime(
                "2001-01-01", "%Y-%m-%d"
            ).date(),
            "height": 65.0,
            "weight": 168.0,
            "gender": ChildGenderEnum.MALE,
            "photo_url": "https://example.com/photo.jpg",
            "illness_history": "Test illness history",
            "medical_diagnoses": "Test medical diagnoses",
        }
        third_data = {
            "id": 3,
            "first_name": "Valerya",
            "last_name": "Konishyna",
            "date_of_birth": datetime.datetime.strptime(
                "2001-01-01", "%Y-%m-%d"
            ).date(),
            "height": 48.0,
            "weight": 160.0,
            "gender": ChildGenderEnum.FEMALE,
            "photo_url": "https://example.com/photo.jpg",
            "illness_history": "Test illness history",
            "medical_diagnoses": "Test medical diagnoses",
        }

        await get_child_repository.add_one(data=second_data)
        await get_child_repository.add_one(data=third_data)

        children = await get_child_repository.get_all()
        assert len(children) == 3

    @pytest.mark.asyncio
    async def test_child_repository_get_one(self, get_child_repository):
        """
        Test ChildRepository get one function
        :param get_child_repository:
        :return:
        """
        child = await get_child_repository.get_one(id=1)

        assert child.first_name == "Vasya"
        assert child.last_name == "Pupkin"
        assert child.date_of_birth == datetime.date(2001, 1, 1)
        assert child.height == 50.0
        assert child.weight == 170.0
        assert child.gender == ChildGenderEnum.MALE
        assert child.photo_url == "https://example.com/photo.jpg"
        assert child.illness_history == "Test illness history"
        assert child.medical_diagnoses == "Test medical diagnoses"

    @pytest.mark.asyncio
    async def test_child_repository_update_one(self, get_child_repository):
        """
        Test ChildRepository get one function
        :param get_child_repository:
        :return:
        """
        data = {
            "id": 1,
            "first_name": "Ilya",
            "last_name": "Pupkin",
            "date_of_birth": datetime.datetime.strptime(
                "2001-01-01", "%Y-%m-%d"
            ).date(),
            "height": 50.0,
            "weight": 170.0,
            "gender": ChildGenderEnum.MALE,
            "photo_url": "https://example.com/photo.jpg",
            "illness_history": "Test some illness history",
            "medical_diagnoses": "Test medical diagnoses",
        }

        child = await get_child_repository.update_one(data=data, id=1)

        assert child.first_name == "Ilya"
        assert child.illness_history == "Test some illness history"

    @pytest.mark.asyncio
    async def test_child_repository_delete_one(self, get_child_repository):
        """
        Test ChildRepository delete one function
        :param get_child_repository:
        :return:
        """
        await get_child_repository.delete_one(id=3)

        children = await get_child_repository.get_all()

        assert len(children) == 2


class TestChildDataRepository:
    """
    TestCase for ChildDataRepository
    """

    @pytest.mark.asyncio
    async def test_child_data_repository_add_one(
        self, get_child_data_repository
    ):
        """
        Test ChildDataRepository add one function
        :return:
        """
        data = {
            "id": 1,
            "date": datetime.datetime.strptime(
                "2024-01-01", "%Y-%m-%d"
            ).date(),
            "feedback": "Состояние хорошее",
            "pulse_recovery_status": ChildPulseRecoveryStatusEnum.GOOD,
            "current_adolescence_age": 24.5,
            "start_adolescence_age": 19.0,
            "peek_adolescence_age": 24.8,
            "end_adolescence_age": 25.4,
            "child_id": 1,
        }

        child_data = await get_child_data_repository.add_one(data=data)

        assert child_data.id == 1
        assert child_data.date == datetime.date(2024, 1, 1)
        assert child_data.feedback == "Состояние хорошее"
        assert (
            child_data.pulse_recovery_status
            == ChildPulseRecoveryStatusEnum.GOOD
        )
        assert child_data.current_adolescence_age == 24.5
        assert child_data.start_adolescence_age == 19.0
        assert child_data.peek_adolescence_age == 24.8
        assert child_data.end_adolescence_age == 25.4
        assert child_data.child_id == 1

    @pytest.mark.asyncio
    async def test_child_data_repository_get_all(
        self, get_child_data_repository
    ):
        """
        Test ChildDataRepository get all function
        :return:
        """
        second_data = {
            "id": 2,
            "date": datetime.datetime.strptime(
                "2024-01-01", "%Y-%m-%d"
            ).date(),
            "feedback": "Состояние хорошее",
            "pulse_recovery_status": ChildPulseRecoveryStatusEnum.GOOD,
            "current_adolescence_age": 24.5,
            "start_adolescence_age": 19.0,
            "peek_adolescence_age": 24.8,
            "end_adolescence_age": 25.4,
            "child_id": 1,
        }
        await get_child_data_repository.add_one(data=second_data)

        child_datas = await get_child_data_repository.get_all()

        assert len(child_datas) == 2

    @pytest.mark.asyncio
    async def test_child_data_repository_get_one(
        self, get_child_data_repository
    ):
        """
        Test ChildDataRepository get one function
        :param get_child_data_repository:
        :return:
        """
        child_data = await get_child_data_repository.get_one(id=1)

        assert child_data.id == 1
        assert child_data.date == datetime.date(2024, 1, 1)
        assert child_data.feedback == "Состояние хорошее"
        assert (
            child_data.pulse_recovery_status
            == ChildPulseRecoveryStatusEnum.GOOD
        )
        assert child_data.current_adolescence_age == 24.5
        assert child_data.start_adolescence_age == 19.0
        assert child_data.peek_adolescence_age == 24.8
        assert child_data.end_adolescence_age == 25.4
        assert child_data.child_id == 1

    @pytest.mark.asyncio
    async def test_child_data_repository_update_one(
        self, get_child_data_repository
    ):
        """
        Test ChildDataRepository update one function
        :param get_child_data_repository:
        :return:
        """
        data = {
            "id": 2,
            "date": datetime.datetime.strptime(
                "2024-01-01", "%Y-%m-%d"
            ).date(),
            "feedback": "Не очень хорошее состояние",
            "pulse_recovery_status": ChildPulseRecoveryStatusEnum.AVERAGE,
            "current_adolescence_age": 24.5,
            "start_adolescence_age": 19.0,
            "peek_adolescence_age": 24.8,
            "end_adolescence_age": 25.4,
            "child_id": 1,
        }

        new_child_data = await get_child_data_repository.update_one(
            data=data, id=2
        )

        assert new_child_data.feedback == "Не очень хорошее состояние"
        assert (
            new_child_data.pulse_recovery_status
            == ChildPulseRecoveryStatusEnum.AVERAGE
        )

    @pytest.mark.asyncio
    async def test_child_data_repository_delete_one(
        self, get_child_data_repository
    ):
        """
        Test ChildDataRepository delete one function
        :param get_child_data_repository:
        :return:
        """
        await get_child_data_repository.delete_one(id=2)

        child_datas = await get_child_data_repository.get_all()

        assert len(child_datas) == 1


class TestChildMedicalDataRepository:
    """
    TestCase for ChildMedicalRepository
    """

    @pytest.mark.asyncio
    async def test_child_medical_data_repository_add_one(
        self, get_child_medical_data_repository
    ):
        """
        Test ChildMedicalDataRepository add one function
        :param get_child_medical_data_repository:
        :return:
        """
        data = {
            "id": 1,
            "date": datetime.datetime.strptime(
                "2024-01-01", "%Y-%m-%d"
            ).date(),
            "vaccinations": "Test vaccinations",
            "medications": "Test medications",
            "procedures": "Test procedures",
            "blood_tests": 10,
            "urine_tests": 10,
            "genetic_test_results": "Test genetic test results",
            "rohrer_index": 15.0,
            "bsa_index": 19,
            "blood_type": ChildBloodTypeEnum.A_POSITIVE,
            "child_id": 1,
        }

        child_medical_data = await get_child_medical_data_repository.add_one(
            data=data
        )

        assert child_medical_data.id == 1
        assert child_medical_data.date == datetime.date(2024, 1, 1)
        assert child_medical_data.vaccinations == "Test vaccinations"
        assert child_medical_data.medications == "Test medications"
        assert child_medical_data.procedures == "Test procedures"
        assert child_medical_data.blood_tests == 10
        assert child_medical_data.urine_tests == 10
        assert (
            child_medical_data.genetic_test_results
            == "Test genetic test results"
        )
        assert child_medical_data.rohrer_index == 15.0
        assert child_medical_data.bsa_index == 19
        assert child_medical_data.blood_type == ChildBloodTypeEnum.A_POSITIVE
        assert child_medical_data.child_id == 1

    @pytest.mark.asyncio
    async def test_child_medical_data_repository_get_all(
        self, get_child_medical_data_repository
    ):
        """
        Test ChildMedicalDataRepository get all function
        :param get_child_medical_data_repository:
        :return:
        """
        second_data = {
            "id": 2,
            "date": datetime.datetime.strptime(
                "2024-03-01", "%Y-%m-%d"
            ).date(),
            "vaccinations": "Test vaccinations",
            "medications": "Test medications",
            "procedures": "Test procedures",
            "blood_tests": 15,
            "urine_tests": 15,
            "genetic_test_results": "Test genetic test results",
            "rohrer_index": 19.0,
            "bsa_index": 20,
            "blood_type": ChildBloodTypeEnum.B_POSITIVE,
            "child_id": 1,
        }
        await get_child_medical_data_repository.add_one(data=second_data)

        child_medical_datas = await get_child_medical_data_repository.get_all()

        assert len(child_medical_datas) == 2

    @pytest.mark.asyncio
    async def test_child_medical_data_repository_get_one(
        self, get_child_medical_data_repository
    ):
        """
        Test ChildMedicalDataRepository get one function
        :param get_child_medical_data_repository:
        :return:
        """
        child_medical_data = await get_child_medical_data_repository.get_one(
            id=1
        )

        assert child_medical_data.id == 1
        assert child_medical_data.date == datetime.date(2024, 1, 1)
        assert child_medical_data.vaccinations == "Test vaccinations"
        assert child_medical_data.medications == "Test medications"
        assert child_medical_data.procedures == "Test procedures"
        assert child_medical_data.blood_tests == 10
        assert child_medical_data.urine_tests == 10
        assert (
            child_medical_data.genetic_test_results
            == "Test genetic test results"
        )
        assert child_medical_data.rohrer_index == 15.0
        assert child_medical_data.bsa_index == 19
        assert child_medical_data.blood_type == ChildBloodTypeEnum.A_POSITIVE
        assert child_medical_data.child_id == 1

    @pytest.mark.asyncio
    async def test_child_medical_data_repository_update_one(
        self, get_child_medical_data_repository
    ):
        """
        Test ChildMedicalDataRepository update one function
        :param get_child_medical_data_repository:
        :return:
        """
        data = {
            "id": 2,
            "date": datetime.datetime.strptime(
                "2024-03-01", "%Y-%m-%d"
            ).date(),
            "vaccinations": "Test vaccinations",
            "medications": "Test medications",
            "procedures": "Test procedures",
            "blood_tests": 15,
            "urine_tests": 15,
            "genetic_test_results": "Test genetic test results",
            "rohrer_index": 19.0,
            "bsa_index": 20,
            "blood_type": ChildBloodTypeEnum.B_NEGATIVE,
            "child_id": 2,
        }

        new_child_medical_data = (
            await get_child_medical_data_repository.update_one(data=data, id=2)
        )

        assert new_child_medical_data.child_id == 2
        assert (
            new_child_medical_data.blood_type == ChildBloodTypeEnum.B_NEGATIVE
        )

    @pytest.mark.asyncio
    async def test_child_medical_data_repository_delete_one(
        self, get_child_medical_data_repository
    ):
        """
        Test ChildMedicalDataRepository delete one function
        :param get_child_medical_data_repository:
        :return:
        """
        await get_child_medical_data_repository.delete_one(id=2)

        child_medical_datas = await get_child_medical_data_repository.get_all()

        assert len(child_medical_datas) == 1


class TestChildHealthDataRepository:
    """
    TestCase for ChildHealthDataRepository
    """

    @pytest.mark.asyncio
    async def test_child_health_data_repository_add_one(
        self, get_child_health_data_repository
    ):
        """
        Test ChildHealthDataRepository add one function
        :param get_child_health_data_repository:
        :return:
        """
        data = {
            "id": 1,
            "date": datetime.datetime.strptime(
                "2024-01-01", "%Y-%m-%d"
            ).date(),
            "current_symptoms": "Test current symptoms",
            "frequency_of_illnesses": "Test frequency of illnesses",
            "doctor_visits": 3,
            "stress_anxiety_depression": "Test stress anxiety depression",
            "emotional_state": ChildEmotionalStateEnum.NOT_BAD,
            "child_id": 1,
        }

        child_health_data = await get_child_health_data_repository.add_one(
            data=data
        )

        assert child_health_data.id == 1
        assert child_health_data.date == datetime.date(2024, 1, 1)
        assert child_health_data.current_symptoms == "Test current symptoms"
        assert (
            child_health_data.frequency_of_illnesses
            == "Test frequency of illnesses"
        )
        assert child_health_data.doctor_visits == 3
        assert (
            child_health_data.stress_anxiety_depression
            == "Test stress anxiety depression"
        )
        assert (
            child_health_data.emotional_state
            == ChildEmotionalStateEnum.NOT_BAD
        )
        assert child_health_data.child_id == 1

    @pytest.mark.asyncio
    async def test_child_health_data_repository_get_all(
        self, get_child_health_data_repository
    ):
        """
        Test ChildHealthDataRepository get all function
        :param get_child_health_data_repository:
        :return:
        """
        second_data = {
            "id": 2,
            "date": datetime.datetime.strptime(
                "2024-01-01", "%Y-%m-%d"
            ).date(),
            "current_symptoms": "Test current symptoms",
            "frequency_of_illnesses": "Test frequency of illnesses",
            "doctor_visits": 3,
            "stress_anxiety_depression": "Test stress anxiety depression",
            "emotional_state": ChildEmotionalStateEnum.HAPPY,
            "child_id": 2,
        }

        await get_child_health_data_repository.add_one(data=second_data)

        child_health_datas = await get_child_health_data_repository.get_all()

        assert len(child_health_datas) == 2

    @pytest.mark.asyncio
    async def test_child_health_data_repository_get_one(
        self, get_child_health_data_repository
    ):
        """
        Test ChildHealthDataRepository get one function
        :param get_child_health_data_repository:
        :return:
        """
        child_health_data = await get_child_health_data_repository.get_one(
            id=1
        )

        assert child_health_data.id == 1
        assert child_health_data.date == datetime.date(2024, 1, 1)
        assert child_health_data.current_symptoms == "Test current symptoms"
        assert (
            child_health_data.frequency_of_illnesses
            == "Test frequency of illnesses"
        )
        assert child_health_data.doctor_visits == 3
        assert (
            child_health_data.stress_anxiety_depression
            == "Test stress anxiety depression"
        )
        assert (
            child_health_data.emotional_state
            == ChildEmotionalStateEnum.NOT_BAD
        )
        assert child_health_data.child_id == 1

    @pytest.mark.asyncio
    async def test_child_health_data_repository_update_one(
        self, get_child_health_data_repository
    ):
        """
        Test ChildHealthDataRepository update one function
        :param get_child_health_data_repository:
        :return:
        """
        data = {
            "id": 2,
            "date": datetime.datetime.strptime(
                "2024-03-01", "%Y-%m-%d"
            ).date(),
            "current_symptoms": "Test current symptoms",
            "frequency_of_illnesses": "Test frequency of illnesses",
            "doctor_visits": 3,
            "stress_anxiety_depression": "Test stress anxiety depression",
            "emotional_state": ChildEmotionalStateEnum.NOT_GOOD,
            "child_id": 2,
        }
        new_child_health_data = (
            await get_child_health_data_repository.update_one(data=data, id=2)
        )

        assert new_child_health_data.date == datetime.date(2024, 3, 1)
        assert (
            new_child_health_data.emotional_state
            == ChildEmotionalStateEnum.NOT_GOOD
        )

    @pytest.mark.asyncio
    async def test_child_health_data_repository_delete_one(
        self, get_child_health_data_repository
    ):
        """
        Test ChildHealthDataRepository delete one function
        :param get_child_health_data_repository:
        :return:
        """
        await get_child_health_data_repository.delete_one(id=2)

        child_health_datas = await get_child_health_data_repository.get_all()

        assert len(child_health_datas) == 1


class TestChildDevelopmentDataRepository:
    """
    TestCase for ChildDevelopmentDataRepository
    """

    @pytest.mark.asyncio
    async def test_child_development_data_repository_add_one(
        self, get_child_development_data_repository
    ):
        """
        Test ChildDevelopmentDataRepository add one function
        :param get_child_development_data_repository:
        :return:
        """
        data = {
            "id": 1,
            "date": datetime.datetime.strptime(
                "2024-01-01", "%Y-%m-%d"
            ).date(),
            "peer_interactions": ChildDevelopmentEnum.NOT_BAD,
            "communication_skills": ChildCommunicationEnum.GOOD,
            "attention_level": ChildDevelopmentEnum.NOT_BAD,
            "memory_level": ChildDevelopmentEnum.NOT_GOOD,
            "problem_solving_skills": ChildDevelopmentEnum.GOOD,
            "cognitive_tests": ChildDevelopmentEnum.NOT_BAD,
            "emotional_tests": ChildDevelopmentEnum.GOOD,
            "child_id": 1,
        }

        child_development_data = (
            await get_child_development_data_repository.add_one(data=data)
        )

        assert child_development_data.id == 1
        assert child_development_data.date == datetime.date(2024, 1, 1)
        assert (
            child_development_data.peer_interactions
            == ChildDevelopmentEnum.NOT_BAD
        )
        assert (
            child_development_data.communication_skills
            == ChildCommunicationEnum.GOOD
        )
        assert (
            child_development_data.attention_level
            == ChildDevelopmentEnum.NOT_BAD
        )
        assert (
            child_development_data.memory_level
            == ChildDevelopmentEnum.NOT_GOOD
        )
        assert (
            child_development_data.problem_solving_skills
            == ChildDevelopmentEnum.GOOD
        )
        assert (
            child_development_data.cognitive_tests
            == ChildDevelopmentEnum.NOT_BAD
        )
        assert (
            child_development_data.emotional_tests == ChildDevelopmentEnum.GOOD
        )
        assert child_development_data.child_id == 1

    @pytest.mark.asyncio
    async def test_child_development_data_repository_get_all(
        self, get_child_development_data_repository
    ):
        """
        Test ChildDevelopmentDataRepository get all function
        :param get_child_development_data_repository:
        :return:
        """
        data = {
            "id": 2,
            "date": datetime.datetime.strptime(
                "2024-01-01", "%Y-%m-%d"
            ).date(),
            "peer_interactions": ChildDevelopmentEnum.NOT_BAD,
            "communication_skills": ChildCommunicationEnum.GOOD,
            "attention_level": ChildDevelopmentEnum.NOT_BAD,
            "memory_level": ChildDevelopmentEnum.NOT_GOOD,
            "problem_solving_skills": ChildDevelopmentEnum.GOOD,
            "cognitive_tests": ChildDevelopmentEnum.NOT_BAD,
            "emotional_tests": ChildDevelopmentEnum.GOOD,
            "child_id": 2,
        }

        await get_child_development_data_repository.add_one(data=data)

        child_development_datas = (
            await get_child_development_data_repository.get_all()
        )

        assert len(child_development_datas) == 2

    async def test_child_development_data_repository_get_one(
        self, get_child_development_data_repository
    ):
        """
        Test ChildDevelopmentDataRepository get one function
        :param get_child_development_data_repository:
        :return:
        """
        child_development_data = (
            await get_child_development_data_repository.get_one(id=1)
        )

        assert child_development_data.id == 1
        assert child_development_data.date == datetime.date(2024, 1, 1)
        assert (
            child_development_data.peer_interactions
            == ChildDevelopmentEnum.NOT_BAD
        )
        assert (
            child_development_data.communication_skills
            == ChildCommunicationEnum.GOOD
        )
        assert (
            child_development_data.attention_level
            == ChildDevelopmentEnum.NOT_BAD
        )
        assert (
            child_development_data.memory_level
            == ChildDevelopmentEnum.NOT_GOOD
        )
        assert (
            child_development_data.problem_solving_skills
            == ChildDevelopmentEnum.GOOD
        )
        assert (
            child_development_data.cognitive_tests
            == ChildDevelopmentEnum.NOT_BAD
        )
        assert (
            child_development_data.emotional_tests == ChildDevelopmentEnum.GOOD
        )
        assert child_development_data.child_id == 1

    async def test_child_development_data_repository_update_one(
        self, get_child_development_data_repository
    ):
        """
        Test ChildDevelopmentDataRepository update one function
        :param get_child_development_data_repository:
        :return:
        """
        data = {
            "id": 2,
            "date": datetime.datetime.strptime(
                "2024-01-01", "%Y-%m-%d"
            ).date(),
            "peer_interactions": ChildDevelopmentEnum.GOOD,
            "communication_skills": ChildCommunicationEnum.GOOD,
            "attention_level": ChildDevelopmentEnum.NOT_BAD,
            "memory_level": ChildDevelopmentEnum.NOT_GOOD,
            "problem_solving_skills": ChildDevelopmentEnum.NOT_BAD,
            "cognitive_tests": ChildDevelopmentEnum.NOT_BAD,
            "emotional_tests": ChildDevelopmentEnum.GOOD,
            "child_id": 2,
        }
        new_child_development_data = (
            await get_child_development_data_repository.update_one(
                data=data, id=2
            )
        )

        assert (
            new_child_development_data.peer_interactions
            == ChildDevelopmentEnum.GOOD
        )
        assert (
            new_child_development_data.problem_solving_skills
            == ChildDevelopmentEnum.NOT_BAD
        )

    async def test_child_development_data_repository_delete_one(
        self, get_child_development_data_repository
    ):
        """
        Test ChildDevelopmentDataRepository delete one function
        :param get_child_development_data_repository:
        :return:
        """
        await get_child_development_data_repository.delete_one(id=2)

        child_development_datas = (
            await get_child_development_data_repository.get_all()
        )

        assert len(child_development_datas) == 1


class TestChildPhysicalDataRepository:
    """
    TestCase for ChildPhysicalDataRepository
    """

    @pytest.mark.asyncio
    async def test_child_physical_data_repository_add_one(
        self, get_child_physical_data_repository
    ):
        """
        Test ChildPhysicalDataRepository add one function
        :param get_child_physical_data_repository:
        :return:
        """
        data = {
            "id": 1,
            "date": datetime.datetime.strptime(
                "2024-01-01", "%Y-%m-%d"
            ).date(),
            "physical_type": "Test physical type",
            "daily_activity_level": 3,
            "flexibility": "Test flexibility",
            "coordination": "Test coordination",
            "injuries_and_chronic_pains": "Test injuries and chronic pains",
            "sports_achievements": "Test sports achievements",
            "interests": "Test interests",
            "child_id": 1,
        }

        child_physical_data = await get_child_physical_data_repository.add_one(
            data=data
        )

        assert child_physical_data.id == 1
        assert child_physical_data.date == datetime.date(2024, 1, 1)
        assert child_physical_data.physical_type == "Test physical type"
        assert child_physical_data.daily_activity_level == 3
        assert child_physical_data.flexibility == "Test flexibility"
        assert child_physical_data.coordination == "Test coordination"
        assert (
            child_physical_data.injuries_and_chronic_pains
            == "Test injuries and chronic pains"
        )
        assert (
            child_physical_data.sports_achievements
            == "Test sports achievements"
        )
        assert child_physical_data.interests == "Test interests"
        assert child_physical_data.child_id == 1

    @pytest.mark.asyncio
    async def test_child_physical_data_repository_get_all(
        self, get_child_physical_data_repository
    ):
        """
        Test ChildPhysicalDataRepository get all function
        :param get_child_physical_data_repository:
        :return:
        """
        second_data = {
            "id": 2,
            "date": datetime.datetime.strptime(
                "2024-01-01", "%Y-%m-%d"
            ).date(),
            "physical_type": "Test physical type",
            "daily_activity_level": 5,
            "flexibility": "Test flexibility",
            "coordination": "Test coordination",
            "injuries_and_chronic_pains": "Test injuries and chronic pains",
            "sports_achievements": "Test sports achievements",
            "interests": "Test interests",
            "child_id": 2,
        }
        await get_child_physical_data_repository.add_one(data=second_data)

        child_physical_datas = (
            await get_child_physical_data_repository.get_all()
        )

        assert len(child_physical_datas) == 2

    @pytest.mark.asyncio
    async def test_child_physical_data_repository_get_one(
        self, get_child_physical_data_repository
    ):
        """
        Test ChildPhysicalDataRepository get one function
        :param get_child_physical_data_repository:
        :return:
        """
        child_physical_data = await get_child_physical_data_repository.get_one(
            id=1
        )

        assert child_physical_data.id == 1
        assert child_physical_data.date == datetime.date(2024, 1, 1)
        assert child_physical_data.physical_type == "Test physical type"
        assert child_physical_data.daily_activity_level == 3
        assert child_physical_data.flexibility == "Test flexibility"
        assert child_physical_data.coordination == "Test coordination"
        assert (
            child_physical_data.injuries_and_chronic_pains
            == "Test injuries and chronic pains"
        )
        assert (
            child_physical_data.sports_achievements
            == "Test sports achievements"
        )
        assert child_physical_data.interests == "Test interests"
        assert child_physical_data.child_id == 1

    @pytest.mark.asyncio
    async def test_child_physical_data_repository_update_one(
        self, get_child_physical_data_repository
    ):
        """
        Test ChildPhysicalDataRepository update one function
        :param get_child_physical_data_repository:
        :return:
        """
        data = {
            "id": 2,
            "date": datetime.datetime.strptime(
                "2024-03-01", "%Y-%m-%d"
            ).date(),
            "physical_type": "Test physical type",
            "daily_activity_level": 10,
            "flexibility": "Test flexibility",
            "coordination": "Test coordination",
            "injuries_and_chronic_pains": "Test injuries and chronic pains",
            "sports_achievements": "Test sports achievements",
            "interests": "Test interests",
            "child_id": 2,
        }

        new_child_physical_data = (
            await get_child_physical_data_repository.update_one(
                data=data, id=2
            )
        )

        assert new_child_physical_data.date == datetime.date(2024, 3, 1)
        assert new_child_physical_data.daily_activity_level == 10

    @pytest.mark.asyncio
    async def test_child_physical_data_repository_delete_one(
        self, get_child_physical_data_repository
    ):
        """
        Test ChildPhysicalDataRepository delete one function
        :param get_child_physical_data_repository:
        :return:
        """
        await get_child_physical_data_repository.delete_one(id=2)

        child_physical_datas = (
            await get_child_physical_data_repository.get_all()
        )

        assert len(child_physical_datas) == 1


class TestChildAcademicDataRepository:
    """
    TestCase for ChildAcademicDataRepository
    """

    @pytest.mark.asyncio
    async def test_child_academic_data_repository_add_one(
        self, get_child_academic_data_repository
    ):
        """
        Test ChildAcademicDataRepository add one function
        :param get_child_academic_data_repository:
        :return:
        """
        data = {
            "id": 1,
            "date": datetime.datetime.strptime(
                "2024-01-01", "%Y-%m-%d"
            ).date(),
            "academic_performance": 9.5,
            "academic_achievements": "Test academic achievements",
            "work_time": 5,
            "attitude_towards_study": ChildTowardStudyEnum.NOT_BAD,
            "areas_of_difficulty": "Test areas of difficulty",
            "additional_support_needs": True,
            "subject_gpa": 20.0,
            "progress_ratio": 20.0,
            "subject_interest": "Test subject interest",
            "child_id": 1,
        }
        child_academic_data = await get_child_academic_data_repository.add_one(
            data=data
        )

        assert child_academic_data.id == 1
        assert child_academic_data.date == datetime.date(2024, 1, 1)
        assert child_academic_data.academic_performance == 9.5
        assert (
            child_academic_data.academic_achievements
            == "Test academic achievements"
        )
        assert child_academic_data.work_time == 5
        assert (
            child_academic_data.attitude_towards_study
            == ChildTowardStudyEnum.NOT_BAD
        )
        assert (
            child_academic_data.areas_of_difficulty
            == "Test areas of difficulty"
        )
        assert child_academic_data.additional_support_needs is True
        assert child_academic_data.subject_gpa == 20.0
        assert child_academic_data.progress_ratio == 20.0
        assert child_academic_data.subject_interest == "Test subject interest"
        assert child_academic_data.child_id == 1

    @pytest.mark.asyncio
    async def test_child_academic_data_repository_get_all(
        self, get_child_academic_data_repository
    ):
        """
        Test ChildAcademicDataRepository get all function
        :param get_child_academic_data_repository:
        :return:
        """
        second_data = {
            "id": 2,
            "date": datetime.datetime.strptime(
                "2024-01-01", "%Y-%m-%d"
            ).date(),
            "academic_performance": 9.7,
            "academic_achievements": "Test academic achievements",
            "work_time": 3,
            "attitude_towards_study": ChildTowardStudyEnum.GOOD,
            "areas_of_difficulty": "Test areas of difficulty",
            "additional_support_needs": False,
            "subject_gpa": 25.0,
            "progress_ratio": 25.0,
            "subject_interest": "Test subject interest",
            "child_id": 2,
        }
        await get_child_academic_data_repository.add_one(data=second_data)

        child_academic_datas = (
            await get_child_academic_data_repository.get_all()
        )

        assert len(child_academic_datas) == 2

    @pytest.mark.asyncio
    async def test_child_academic_data_repository_get_one(
        self, get_child_academic_data_repository
    ):
        """
        Test ChildAcademicDataRepository get one function
        :param get_child_academic_data_repository:
        :return:
        """
        child_academic_data = await get_child_academic_data_repository.get_one(
            id=1
        )

        assert child_academic_data.id == 1
        assert child_academic_data.date == datetime.date(2024, 1, 1)
        assert child_academic_data.academic_performance == 9.5
        assert (
            child_academic_data.academic_achievements
            == "Test academic achievements"
        )
        assert child_academic_data.work_time == 5
        assert (
            child_academic_data.attitude_towards_study
            == ChildTowardStudyEnum.NOT_BAD
        )
        assert (
            child_academic_data.areas_of_difficulty
            == "Test areas of difficulty"
        )
        assert child_academic_data.additional_support_needs is True
        assert child_academic_data.subject_gpa == 20.0
        assert child_academic_data.progress_ratio == 20.0
        assert child_academic_data.subject_interest == "Test subject interest"
        assert child_academic_data.child_id == 1

    @pytest.mark.asyncio
    async def test_child_academic_data_repository_update_one(
        self, get_child_academic_data_repository
    ):
        """
        Test ChildAcademicDataRepository update one function
        :param get_child_academic_data_repository:
        :return:
        """
        data = {
            "id": 2,
            "date": datetime.datetime.strptime(
                "2024-01-01", "%Y-%m-%d"
            ).date(),
            "academic_performance": 9.7,
            "academic_achievements": "Test academic achievements",
            "work_time": 2,
            "attitude_towards_study": ChildTowardStudyEnum.NOT_BAD,
            "areas_of_difficulty": "Test areas of difficulty",
            "additional_support_needs": False,
            "subject_gpa": 22.4,
            "progress_ratio": 25.0,
            "subject_interest": "Test subject interest",
            "child_id": 2,
        }

        new_child_academic_data = (
            await get_child_academic_data_repository.update_one(
                data=data, id=2
            )
        )

        assert new_child_academic_data.work_time == 2
        assert new_child_academic_data.subject_gpa == 22.4
        assert (
            new_child_academic_data.attitude_towards_study
            == ChildTowardStudyEnum.NOT_BAD
        )

    @pytest.mark.asyncio
    async def test_child_academic_data_repository_delete_one(
        self, get_child_academic_data_repository
    ):
        """
        Test ChildAcademicDataRepository delete one function
        :param get_child_academic_data_repository:
        :return:
        """
        await get_child_academic_data_repository.delete_one(id=2)

        child_academic_datas = (
            await get_child_academic_data_repository.get_all()
        )

        assert len(child_academic_datas) == 1


class TestChildFamilyDataRepository:
    """
    TestCase for ChildFamilyDataRepository
    """

    @pytest.mark.asyncio
    async def test_child_family_data_repository_add_one(
        self, get_child_family_data_repository
    ):
        """
        Test ChildFamilyDataRepository add one function
        :param get_child_family_data_repository:
        :return:
        """
        data = {
            "id": 1,
            "date": datetime.datetime.strptime(
                "2024-01-01", "%Y-%m-%d"
            ).date(),
            "family_info": "Test family info",
            "family_involvement": "Test family involvement",
            "parenting_methods": ChildParentingMethodsEnum.SUPPORTIVE,
            "behavior_and_discipline": ChildBehaviorDisciplineEnum.GOOD,
            "parental_attention_and_care": ChildParentalAttentionEnum.GOOD,
            "child_id": 1,
        }
        child_family_data = await get_child_family_data_repository.add_one(
            data=data
        )

        assert child_family_data.id == 1
        assert child_family_data.date == datetime.date(2024, 1, 1)
        assert child_family_data.family_info == "Test family info"
        assert (
            child_family_data.family_involvement == "Test family involvement"
        )
        assert (
            child_family_data.parenting_methods
            == ChildParentingMethodsEnum.SUPPORTIVE
        )
        assert (
            child_family_data.behavior_and_discipline
            == ChildBehaviorDisciplineEnum.GOOD
        )
        assert (
            child_family_data.parental_attention_and_care
            == ChildParentalAttentionEnum.GOOD
        )
        assert child_family_data.child_id == 1

    @pytest.mark.asyncio
    async def test_child_family_data_repository_get_all(
        self, get_child_family_data_repository
    ):
        """
        Test ChildFamilyDataRepository get all function
        :param get_child_family_data_repository:
        :return:
        """
        second_data = {
            "id": 2,
            "date": datetime.datetime.strptime(
                "2024-01-01", "%Y-%m-%d"
            ).date(),
            "family_info": "Test family info",
            "family_involvement": "Test family involvement",
            "parenting_methods": ChildParentingMethodsEnum.SUPPORTIVE,
            "behavior_and_discipline": ChildBehaviorDisciplineEnum.EXCELLENT,
            "parental_attention_and_care": ChildParentalAttentionEnum.NOT_BAD,
            "child_id": 2,
        }
        await get_child_family_data_repository.add_one(data=second_data)

        child_family_datas = await get_child_family_data_repository.get_all()

        assert len(child_family_datas) == 2

    @pytest.mark.asyncio
    async def test_child_family_data_repository_get_one(
        self, get_child_family_data_repository
    ):
        """
        Test ChildFamilyDataRepository get one function
        :param get_child_family_data_repository:
        :return:
        """
        child_family_data = await get_child_family_data_repository.get_one(
            id=1
        )

        assert child_family_data.id == 1
        assert child_family_data.date == datetime.date(2024, 1, 1)
        assert child_family_data.family_info == "Test family info"
        assert (
            child_family_data.family_involvement == "Test family involvement"
        )
        assert (
            child_family_data.parenting_methods
            == ChildParentingMethodsEnum.SUPPORTIVE
        )
        assert (
            child_family_data.behavior_and_discipline
            == ChildBehaviorDisciplineEnum.GOOD
        )
        assert (
            child_family_data.parental_attention_and_care
            == ChildParentalAttentionEnum.GOOD
        )
        assert child_family_data.child_id == 1

    @pytest.mark.asyncio
    async def test_child_family_data_repository_update_one(
        self, get_child_family_data_repository
    ):
        """
        Test ChildFamilyDataRepository update one function
        :param get_child_family_data_repository:
        :return:
        """
        data = {
            "id": 2,
            "date": datetime.datetime.strptime(
                "2024-01-01", "%Y-%m-%d"
            ).date(),
            "family_info": "Test family info",
            "family_involvement": "Test family involvement",
            "parenting_methods": ChildParentingMethodsEnum.STRICT,
            "behavior_and_discipline": ChildBehaviorDisciplineEnum.NEEDS_IMPROVEMENT,
            "parental_attention_and_care": ChildParentalAttentionEnum.NOT_GOOD,
            "child_id": 2,
        }
        new_child_family_data = (
            await get_child_family_data_repository.update_one(data=data, id=2)
        )

        assert (
            new_child_family_data.parenting_methods
            == ChildParentingMethodsEnum.STRICT
        )
        assert (
            new_child_family_data.behavior_and_discipline
            == ChildBehaviorDisciplineEnum.NEEDS_IMPROVEMENT
        )
        assert (
            new_child_family_data.parental_attention_and_care
            == ChildParentalAttentionEnum.NOT_GOOD
        )

    @pytest.mark.asyncio
    async def test_child_family_data_repository_delete_one(
        self, get_child_family_data_repository
    ):
        """
        Test ChildFamilyDataRepository delete one function
        :param get_child_family_data_repository:
        :return:
        """
        await get_child_family_data_repository.delete_one(id=2)

        child_family_datas = await get_child_family_data_repository.get_all()

        assert len(child_family_datas) == 1


class TestChildNutritionDataRepository:
    """
    TestCase for ChildNutritionDataRepository
    """

    @pytest.mark.asyncio
    async def test_child_nutrition_data_repository_add_one(
        self, get_child_nutrition_data_repository
    ):
        """
        Test ChildNutritionDataRepository add one function
        :param get_child_nutrition_data_repository:
        :return:
        """
        data = {
            "id": 1,
            "date": datetime.datetime.strptime(
                "2024-01-01", "%Y-%m-%d"
            ).date(),
            "dietary_info": "Test dietary info",
            "snacking_habits": True,
            "beverage_consumption": True,
            "supplements_or_vitamins": "Test supplements with vitamins",
            "reactions_to_food": "Test reactions to food",
            "allergies_or_intolerances": "Test allergies with intolerances",
            "child_id": 1,
        }
        child_nutrition_data = (
            await get_child_nutrition_data_repository.add_one(data=data)
        )

        assert child_nutrition_data.id == 1
        assert child_nutrition_data.date == datetime.date(2024, 1, 1)
        assert child_nutrition_data.dietary_info == "Test dietary info"
        assert child_nutrition_data.snacking_habits is True
        assert child_nutrition_data.beverage_consumption is True
        assert (
            child_nutrition_data.supplements_or_vitamins
            == "Test supplements with vitamins"
        )
        assert (
            child_nutrition_data.reactions_to_food == "Test reactions to food"
        )
        assert (
            child_nutrition_data.allergies_or_intolerances
            == "Test allergies with intolerances"
        )
        assert child_nutrition_data.child_id == 1

    @pytest.mark.asyncio
    async def test_child_nutrition_data_repository_get_all(
        self, get_child_nutrition_data_repository
    ):
        """
        Test ChildNutritionDataRepository get all function
        :param get_child_nutrition_data_repository:
        :return:
        """
        second_data = {
            "id": 2,
            "date": datetime.datetime.strptime(
                "2024-01-01", "%Y-%m-%d"
            ).date(),
            "dietary_info": "Test dietary info",
            "snacking_habits": True,
            "beverage_consumption": True,
            "supplements_or_vitamins": "Test supplements with vitamins",
            "reactions_to_food": "Test reactions to food",
            "allergies_or_intolerances": "Test allergies with intolerances",
            "child_id": 2,
        }
        await get_child_nutrition_data_repository.add_one(data=second_data)

        child_nutrition_datas = (
            await get_child_nutrition_data_repository.get_all()
        )

        assert len(child_nutrition_datas) == 2

    @pytest.mark.asyncio
    async def test_child_nutrition_data_repository_get_one(
        self, get_child_nutrition_data_repository
    ):
        """
        Test ChildNutritionDataRepository get one function
        :param get_child_nutrition_data_repository:
        :return:
        """
        child_nutrition_data = (
            await get_child_nutrition_data_repository.get_one(id=1)
        )

        assert child_nutrition_data.id == 1
        assert child_nutrition_data.date == datetime.date(2024, 1, 1)
        assert child_nutrition_data.dietary_info == "Test dietary info"
        assert child_nutrition_data.snacking_habits is True
        assert child_nutrition_data.beverage_consumption is True
        assert (
            child_nutrition_data.supplements_or_vitamins
            == "Test supplements with vitamins"
        )
        assert (
            child_nutrition_data.reactions_to_food == "Test reactions to food"
        )
        assert (
            child_nutrition_data.allergies_or_intolerances
            == "Test allergies with intolerances"
        )
        assert child_nutrition_data.child_id == 1

    @pytest.mark.asyncio
    async def test_child_nutrition_data_repository_update_one(
        self, get_child_nutrition_data_repository
    ):
        """
        Test ChildNutritionDataRepository update one function
        :param get_child_nutrition_data_repository:
        :return:
        """
        data = {
            "id": 2,
            "date": datetime.datetime.strptime(
                "2024-01-01", "%Y-%m-%d"
            ).date(),
            "dietary_info": "Test dietary info",
            "snacking_habits": False,
            "beverage_consumption": False,
            "supplements_or_vitamins": "Test supplements with vitamins",
            "reactions_to_food": "Test reactions to food",
            "allergies_or_intolerances": "Test allergies with intolerances",
            "child_id": 2,
        }
        new_child_nutrition_data = (
            await get_child_nutrition_data_repository.update_one(
                data=data, id=2
            )
        )

        assert new_child_nutrition_data.snacking_habits is False
        assert new_child_nutrition_data.beverage_consumption is False

    @pytest.mark.asyncio
    async def test_child_nutrition_data_repository_delete_one(
        self, get_child_nutrition_data_repository
    ):
        """
        Test ChildNutritionDataRepository delete one function
        :param get_child_nutrition_data_repository:
        :return:
        """
        await get_child_nutrition_data_repository.delete_one(id=2)

        child_nutrition_datas = (
            await get_child_nutrition_data_repository.get_all()
        )

        assert len(child_nutrition_datas) == 1
