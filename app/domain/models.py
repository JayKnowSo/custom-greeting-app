


from sqlmodel import SQLModel, Field
from typing import Optional
from pydantic import StrictStr, StrictInt, computed_field


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    hashed_password: str
    role: str


class SessionModel(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    username: StrictStr
    greetings: StrictInt
    number: StrictInt
    farewell: StrictStr

    @computed_field
    @property
    def result(self) -> int:
        return self.greetings * self.number
