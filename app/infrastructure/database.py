import os
from dotenv import load_dotenv
from sqlmodel import SQLModel, Field, create_engine, Session
from typing import Optional

# Load environment variables from a .env file
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set.")

# Create the database engine (PostgreSQL)
engine = create_engine(
    DATABASE_URL,
    echo=True,
    pool_pre_ping=True
) 

class SessionRecord(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    greetings: str  # Changed from int to str if it's a greeting message
    number: int # Changed from int to str if it's a number in string format
    farewell: str

def create_db():
    """
    Function to create all tables in the database.
    This should be run once to initialize the schema.
    """
    SQLModel.metadata.create_all(engine)

# Dependency function to get a database session
def get_db():
    """
    Dependency to get a database session.
    Automatically closes the session after use.
    """
    with Session(engine) as session:
        yield session