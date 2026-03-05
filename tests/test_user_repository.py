


from app.domain.models import User
from app.security.password import hash_password




def test_add_user(user_repository):
    user = User(
        username="TestUser1",
        hashed_password=hash_password("testpassword"),  # MUST match model field
        role="admin"
    )
    saved = user_repository.add(user)
    assert saved.id is not None
    assert saved.username == "TestUser1"

def test_get_by_username(user_repository):
    user = User(
        username="TestUser2",
        hashed_password=hash_password("testpassword"),  # MUST match model field
        role="admin"
    )
    user_repository.add(user)
    retrieved = user_repository.get_by_username("TestUser2")
    assert retrieved is not None
    assert retrieved.username == "TestUser2"