from re import compile

PASSWORD_REGEX = compile(
    r"^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,64}$"
)


def password_validator(password: str) -> str:
    """
    Custom validator checking valid input password
    :param password:
    :return:
    """
    if PASSWORD_REGEX.fullmatch(password) is None:
        raise ValueError("Invalid password")
    return password


def is_alpha_validator(value: str) -> str:
    """
    Custom validator checking valid input value, which should be string
    :param value:
    :return:
    """
    if not value.isalpha():
        raise ValueError("Invalid value")
    return value
