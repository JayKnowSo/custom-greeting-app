


# conftest.py
import pytest
from sqlmodel import SQLModel, create_engine, Session as DBSession
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient

from app.main import app
from app.infrastructure.database import get_db
from app.infrastructure.db_repository import SQLSessionRepository, UserRepository

TEST_DATABASE_URL = "sqlite:///:memory:"

@pytest.fixture(name="session")
def session_fixture():
    test_engine = create_engine(
        TEST_DATABASE_URL,
        echo=False,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    SQLModel.metadata.create_all(test_engine)

    with DBSession(test_engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: DBSession):
    def override_get_db():
        yield session

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def user_repository(session: DBSession):
    return UserRepository(session)


@pytest.fixture
def session_repository(session: DBSession):
    return SQLSessionRepository(session)