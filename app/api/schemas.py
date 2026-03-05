# This file defines the Pydantic models for request and response validation in the API endpoints.
# The `SessionCreateRequest` model is used to validate the incoming data when creating a new greeting session,
#  ensuring that all required fields are present and of the correct type.
# The `SessionResponse` model is used to structure the response data when returning session information,
# allowing for clear and consistent API responses that can be easily consumed by clients.

from pydantic import BaseModel, ConfigDict


class SessionCreate(BaseModel):
    username: str
    greetings: int
    number: int
    farewell: str

class SessionResponse(BaseModel):
    id: int
    username: str
    greetings: int
    number: int
    farewell: str
    result: int

    model_config = ConfigDict(from_attributes=True)

# This model is used for the login endpoint, 
# validating that the incoming request contains both a username and a password.
class LoginRequest(BaseModel):
    username: str
    password: str