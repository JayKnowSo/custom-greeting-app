from typing import Optional
from sqlmodel import SQLModel, Field


# Request model (used for POST)
class SessionCreate(SQLModel):
    name: str
    greetings: int
    number: int
    farewell: str


# Database + Response model
class SessionModel(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    greetings: int
    number: int
    farewell: str