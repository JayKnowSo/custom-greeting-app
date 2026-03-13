import pytest

from app.infrastructure.functions import greet, custom_farewell, find_sessions_by_name
from pydantic import ValidationError
from app.domain.models import SessionModel
from typing import List, Dict, Any

# This test file is designed to verify the functionality of the functions defined in the app.infrastructure.functions module.
def test_greet():
    result = greet("Alice", 3)
    assert result == ["Hello, Alice!"] * 3

# This test verifies that the custom_farewell function correctly formats a farewell message with the given name and farewell message.
def test_custom_farewell():
    result = custom_farewell("Bob", "Bye")
    assert result == "Bye, Bob!"

# This test verifies that the find_sessions_by_name function correctly finds sessions by name, ignoring case.
def test_find_sessions_by_name():
    # Explicitly telling the linter this is a list of dicts
    sessions: List[Dict[str, Any]] = [
        {"username": "Alice", "greetings": 2, "number": 5}
    ]
    result = find_sessions_by_name(sessions, "alice")
    assert len(result) == 1

# This test verifies that the SessionModel raises validation errors when given incorrect types for its fields.
def test_session_model_good():
    session = SessionModel(
        username="Alice",
        greetings=3,
        number=5,
        farewell="Goodbye"
    )

    assert session.username == "Alice"
    assert session.greetings == 3
    assert session.number == 5
    assert session.farewell == "Goodbye"
    assert session.result == 15 # 3 * 5 = 15
    print("Session model properties are correct.")


 # This test verifies that the SessionModel raises validation errors when given incorrect types for its fields.
def test_session_model_bad_details():
    with pytest.raises(ValidationError):
        SessionModel.model_validate(
        {
            "username": None,
            "greetings": "three",
            "number": "five",
            "farewell": None
        }
        )
