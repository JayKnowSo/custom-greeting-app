

"""
app/domain/models.py
=====================
Domain models — the core business objects of the application.
These are the single source of truth for data structure.

SQLModel combines SQLAlchemy (database ORM) and Pydantic (validation)
into one class. One definition handles both database tables AND
API request/response validation.

Why domain models matter:
In clean architecture the domain layer owns the business rules.
Models live here — not in infrastructure (database.py).
database.py should only handle connection and engine setup.
All table definitions belong here.
"""

from sqlmodel import SQLModel, Field
from typing import Optional
from pydantic import StrictStr, StrictInt, computed_field


class User(SQLModel, table=True):
    """
    Represents an authenticated user in the system.

    table=True tells SQLModel to create a real database table.
    Without table=True it's just a Pydantic validation model.

    Fields:
        id:              auto-incremented primary key
        username:        unique login identifier
        hashed_password: bcrypt hash — never store plaintext passwords
        role:            RBAC role — admin, user, or readonly
                         controls what endpoints the user can access
    """

    # Optional[int] = None means the DB auto-assigns this
    # Never set id manually — let the database handle it
    id: Optional[int] = Field(default=None, primary_key=True)

    # index=True creates a database index on username
    # Makes lookups by username fast — O(log n) instead of O(n)
    # unique=True enforces no duplicate usernames at the DB level
    username: str = Field(index=True, unique=True)

    # NEVER store plaintext passwords
    # AuthService hashes passwords with bcrypt before storing
    # bcrypt is one-way — you can verify but never reverse it
    hashed_password: str

    # Role controls access via RBAC (Role-Based Access Control)
    # admin    → full access including /clear
    # user     → can create sessions, search
    # readonly → can only read/search
    role: str = Field(default="user")


class SessionModel(SQLModel, table=True):
    """
    Represents a greeting session created by a user.

    Uses StrictStr and StrictInt from Pydantic for strict type validation.
    StrictStr rejects integers passed as strings.
    StrictInt rejects floats passed as integers.
    This prevents type coercion attacks.

    Fields:
        id:        auto-incremented primary key
        username:  who created the session
        greetings: how many greetings (0-1000)
        number:    the number for multiplication (0-10000)
        farewell:  the farewell message (1-100 chars)
        result:    computed field — greetings * number
                   calculated automatically, never stored in DB
    """

    id: Optional[int] = Field(default=None, primary_key=True)

    # StrictStr = rejects non-string types at validation time
    # Prevents type confusion attacks
    username: StrictStr

    # StrictInt = rejects floats, strings, booleans
    # 1.5 → rejected. "5" → rejected. True → rejected.
    greetings: StrictInt

    number: StrictInt

    farewell: StrictStr

    @computed_field
    @property
    def result(self) -> int:
        """
        Computed field — calculated on the fly, never stored in DB.

        @computed_field tells Pydantic to include this in serialization
        @property makes it a read-only attribute (no setter)

        Why computed not stored:
        Storing derived data creates sync issues.
        If greetings or number changes, result must update too.
        Computing it fresh every time guarantees correctness.
        """
        return self.greetings * self.number
