# tests/test_models.py
# This file contains tests for the data models used in the application.
# The tests ensure that the models can be correctly instantiated and that their methods (like serialization) work as expected.


from app.domain.models import SessionModel


def test_session_model_serialization():
    data = {
        "username": "Alice",
        "greetings": 3,
        "number": 5,
        "farewell": "Goodbye"
    }

    session = SessionModel(**data)

    serialized = session.model_dump()

    assert "result" in serialized
    assert serialized["result"] == 15
    assert serialized["username"] == "Alice"