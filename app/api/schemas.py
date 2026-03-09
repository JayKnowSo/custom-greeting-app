# This file defines the Pydantic models for request and response validation in the API endpoints.
# The `SessionCreateRequest` model is used to validate the incoming data when creating a new greeting session,
#  ensuring that all required fields are present and of the correct type.
# The `SessionResponse` model is used to structure the response data when returning session information,
# allowing for clear and consistent API responses that can be easily consumed by clients.

from pydantic import BaseModel, ConfigDict, Field, field_validator


class SessionCreate(BaseModel):
    model_config = ConfigDict(
        # Reject any fields not defined in this schema
        # Attacker sends {"username": "x", "is_admin": true} → rejected
        extra="forbid",
        # Strip leading/trailing whitespace from all string fields
        str_strip_whitespace=True,
    )

    username: str = Field(
        min_length=1,
        max_length=50,
        description="Username must be 1-50 characters"
    )
    greetings: int = Field(
        ge=0,
        le=1000,
        description="Greetings count must be between 0 and 1000"
    )
    number: int = Field(
        ge=0,
        le=10000,
        description="Number must be between 0 and 10000"
    )
    farewell: str = Field(
        min_length=1,
        max_length=100,
        description="Farewell must be 1-100 characters"
    )

    @field_validator("username")
    @classmethod
    def username_no_special_chars(cls, v: str) -> str:
        """
        Block characters commonly used in injection attacks.
        A username should never contain < > ; ' " -- or script tags.
        """
        forbidden = ["<", ">", ";", "'", '"', "--", "/*", "*/", "script"]
        for char in forbidden:
            if char.lower() in v.lower():
                raise ValueError(
                    f"Username contains forbidden character: {char}"
                )
        return v


class SessionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    greetings: int
    number: int
    farewell: str
    result: int


class LoginRequest(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
    )

    username: str = Field(
        min_length=1,
        max_length=50,
        description="Username must be 1-50 characters"
    )
    password: str = Field(
        min_length=8,
        max_length=72,
        description="Password must be 8-72 characters"
    )