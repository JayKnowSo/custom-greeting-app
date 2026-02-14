from sqlmodel import SQLModel, Field, create_engine, Session, select

# This file contains the database model and functions to interact with the database.
# The SessionRecord class represents a record in the database, and the create_db function creates the database and the table if it doesn't exist.
# The engine is created using SQLite, and the database file is named greetings.db.
# Database table model
class SessionRecord(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    greetings: int
    multiplication_number: int
    farewell: str

# Create the database engine
# The create_engine function is used to create a connection to the SQLite database. The database file will be created in the same directory as the script if it doesn't already exist.
# The connection string "sqlite:///greetings.db" specifies that we are using SQLite and the database file is greetings.db.
# The three slashes indicate that the database file is located in the current directory. If you wanted to specify a different path, you could use something like "sqlite:///path/to/greetings.db".
# For example, if you wanted to create the database in a subdirectory called "data", you could use "sqlite:///data/greetings.db". If the "data" directory does not exist, it will be created automatically when the database is created.
# SQLite is a lightweight, file-based database that is easy to set up and use, making it a good choice for small applications or for development purposes. It does not require a separate server process and allows you to store the entire database in a single file on disk.
# In this case, we are using SQLite for simplicity, but in a production environment, you might want to use a more robust database system like PostgreSQL or MySQL.
#SQLite engine creation
engine = create_engine("sqlite:///greetings.db")

# Function to create the database and the table if it doesn't exist
# The create_db function uses the SQLModel.metadata.create_all method to create the database and the table based on the SessionRecord model. If the database file already exists, it will not be overwritten, and if the table already exists, it will not be recreated.
def create_db():
    SQLModel.metadata.create_all(engine)
