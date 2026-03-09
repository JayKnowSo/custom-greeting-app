


import os
from dotenv import load_dotenv
from sqlmodel import SQLModel, Field, create_engine, Session
from typing import Optional
from sqlalchemy import Column, JSON
from pydantic import field_validator

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test_local.db")
print("DATABASE_URL =", DATABASE_URL)

if "sqlite" in DATABASE_URL:
    engine = create_engine(
        DATABASE_URL,
        echo=True,
        connect_args={"check_same_thread": False}
    )
else:
    engine = create_engine(
        DATABASE_URL,
        echo=True,
        pool_pre_ping=True
    )


class SessionRecord(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    greetings: int
    number: int
    farewell: str

    @field_validator("greetings", "number")
    def must_be_positive(cls, v):
        if v < 0:
            raise ValueError("Must be positive")
        return v


def create_db():
    SQLModel.metadata.create_all(engine)


def get_db():
    with Session(engine) as session:
        yield session


class UserRecord(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    hashed_password: str
    role: str = Field(default="user")