from typing import Annotated

from pydantic import AfterValidator

from src.schemas.custom_validators import (
    password_validator,
    is_alpha_validator,
)

# Initial custom types
PasswordStr = Annotated[str, AfterValidator(password_validator)]
AlphaStr = Annotated[str, AfterValidator(is_alpha_validator)]
