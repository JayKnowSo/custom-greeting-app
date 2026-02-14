# This test file is designed to verify the functionality of the services defined in the app.domain.services module.
# The tests include creating a session record in the database and retrieving all sessions.
# The test_create_and_read_session_db function tests the creation of a session record using the create_session_record function and then retrieves all sessions from the database using the get_all_sessions_from_db function to ensure that the newly created session is present in the database.
# The tests use assertions to check that the session record has been created with the correct attributes and that it can be retrieved successfully from the database.
# The test assumes that the database is properly set up and that the create_session_record and get_all_sessions_from_db functions are implemented correctly in the app.domain.services module.

from app.domain.services import create_session_record, get_all_sessions_from_db


def test_create_and_read_session_db():

    # create
    record = create_session_record(
        name="TestUser",
        greetings=2,
        number=7,
        farewell="Bye"
    )

    assert record.id is not None
    assert record.name == "TestUser"

    # read
    sessions = get_all_sessions_from_db()

    assert any(s.name == "TestUser" for s in sessions)
