from enum import Enum


class UserRoleEnum(Enum):
    """
    Enum class for User role
    """

    PARENT = "parent"
    COACH = "coach"


class UserSportTypeEnum(Enum):
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


class ChildGenderEnum(Enum):
    """
    Enum class for Child gender
    """

    MALE = "Male"
    FEMALE = "Female"


class ChildBloodTypeEnum(Enum):
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


class ChildEmotionalStateEnum(Enum):
    """
    Enum class for Child emotional state
    """

    HAPPY = "Happy"
    NOT_BAD = "Not bad"
    NOT_GOOD = "Not good"
    BAD = "Bad"


class ChildDevelopmentEnum(Enum):
    """
    Basic enum class for all fields of ChildDevelopment model
    """

    GOOD = "Good"
    NOT_BAD = "Not bad"
    NOT_GOOD = "Not good"
    BAD = "Bad"


class ChildCommunicationEnum(Enum):
    """
    Enum class for Child communication skills
    """

    BOOLING = "Booling"
    GOOD = "Good"
    NOT_BAD = "Not bad"
    NOT_GOOD = "Not good"
    BAD = "Bad"


class ChildTowardStudyEnum(Enum):
    """
    Enum class for Child toward study
    """

    GOOD = "Good"
    NOT_BAD = "Not bad"
    NOT_GOOD = "Not good"
    BAD = "Bad"


class ChildParentingMethodsEnum(Enum):
    """
    Enum class of Child parenting methods
    """

    STRICT = "Строгое воспитание"
    SUPPORTIVE = "Поддерживающее воспитание"
    LENIENT = "Мягкое воспитание"
    INVOLVED = "Вовлечённое воспитание"
    CARELESS = "Беспечное воспитание"


class ChildParentalAttentionEnum(Enum):
    """
    Enum class of Child parental attention
    """

    GOOD = "Good"
    NOT_BAD = "Not bad"
    NOT_GOOD = "Not good"
    BAD = "Bad"

class PulseRecoveryStatus(Enum):
    GOOD = "Хорошо"
    AVERAGE = "Средне"
    POOR = "Плохо"
    ERROR = "Ошибка в замере: пульс в положении стоя не может быть меньше пульса в положении лёжа. Пожалуйста, перепроверьте замер и повторите запись."