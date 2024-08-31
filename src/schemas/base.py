from pydantic import BaseModel, ConfigDict


class DTO(BaseModel):
    """
    Base schema
    """

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        str_strip_whitespace=True,
        from_attributes=True,
    )
