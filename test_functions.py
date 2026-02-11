from functions import greet, custom_farewell, find_sessions_by_name, Session_Model
from pydantic import ValidationError

def test_greet():
    result = greet("Alice", 3)
    assert result == ["Hello, Alice!"] * 3

def test_custom_farewell():
    result = custom_farewell("Bob", "Bye")
    assert result == "Bye, Bob!"

def test_find_sessions_by_name():
    sessions = [{"name": "Alice", "greetings": 2, "multiplication_number": 5}]
    result = find_sessions_by_name(sessions, "alice")
    assert len(result) == 1

def test_session_model_good():
    session = SessionModel(
        name="Alice",
        greetings=3,
        multiplication_number=5,
        multiplication_table=["5 x 1 = 5", "5 x 2 = 10"],
        farewell="Goodbye"
    )
    assert session.name == "Alice"

def test_session_model_bad():
    try:
        SessionModel(
            name=123,
            greetings="three",
            multiplication_number="five",
            multiplication_table="5 x 1 = 5",
            farewell=99
        )
        assert False, "ValidationError was not raised"
    except ValidationError:
        pass  # test passes if exception is raised

try:
    good_session = SessionModel(
        name="Alice",
        greetings=3,
        multiplication_number=5,
        multiplication_table=["5 x 1 = 5", "5 x 2 = 10"],
        farewell="Goodbye"
    )
    print("Good session works:", good_session)
except ValidationError as e:
    print(e)

try:
     bad_session = SessionModel(
        name=123,                 # should be str
        greetings="three",        # should be int
        multiplication_number="five",  # should be int
        multiplication_table="5 x 1 = 5", # should be list[str]
        farewell=99               # should be str
    )
except ValidationError as e:
    print("Validation error caught!")
    print(e)
