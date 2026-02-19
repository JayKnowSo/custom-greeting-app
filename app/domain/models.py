# app/domain/models.py
# This file defines the data models for the Greeting App, 
# including the SessionModel class and the save_table_to_file function.
# The SessionModel class represents the structure of a greeting session,
# while the save_table_to_file function is responsible for saving session data to a file or database


from pydantic import BaseModel

class SessionModel(BaseModel):
    name: str
    greetings: int
    number: int
    farewell: str