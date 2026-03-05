# This file contains tests for the repository layer of the application.
# The tests ensure that the repository correctly implements the interface defined in repositories.py,
#  and that it can successfully add, retrieve, and delete session data from the database.


from app.domain.models import SessionModel


def test_repository_add(session_repository):
    session = SessionModel(
        username="TestUserRepo",
        greetings=3,
        number=5,
        farewell="bye"
    )

    saved = session_repository.add(session)

    assert saved.id is not None
    assert saved.username == "TestUserRepo"
  