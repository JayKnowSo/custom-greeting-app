# This file defines the Pydantic models for request and response validation in the API endpoints.
# The `SessionCreateRequest` model is used to validate the incoming data when creating a new greeting session,
#  ensuring that all required fields are present and of the correct type.
# The `SessionResponse` model is used to structure the response data when returning session information,
# allowing for clear and consistent API responses that can be easily consumed by clients.

from pydantic import BaseModel


class SessionCreate(BaseModel):
    name: str
    greetings: int
    number: int
    farewell: str

class SessionResponse(BaseModel):
    id: int
    name: str
    greetings: int
    number: int
    farewell: str

    class Config:
        from_attributes = True