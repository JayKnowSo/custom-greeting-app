import os
from dotenv import load_dotenv
from sqlmodel import SQLModel, Field, create_engine, Session

# Load environment variables from a .env file
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set.")


# Create the database engine
# postgreSQL engine

engine = create_engine(DATABASE_URL, echo=True) # Shows SQL queries in terminal (great for learning)

# This file contains the database model and functions to interact with the database.
# The SessionRecord class represents a record in the database, and the create_db function creates the database and the table if it doesn't exist.
# The engine is created using SQLite, and the database file is named greetings.db.
# Database table model
class SessionRecord(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    greetings: int
    number: int
    farewell: str

# Function to create the database and the table if it doesn't exist
# The create_db function uses the SQLModel.metadata.create_all method to create the database and the table based on the SessionRecord model. If the database file already exists, it will not be overwritten, and if the table already exists, it will not be recreated.
def create_db():
    SQLModel.metadata.create_all(engine)

# Dependency function to get a database session
def get_db():
    with Session(engine) as session:
        yield session