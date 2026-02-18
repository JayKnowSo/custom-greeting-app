# API endpoints for Greeting App using FastAPI
# This file defines the API routes and handlers for the Greeting App, allowing clients to interact with the app's functionality over HTTP.
# It uses FastAPI to create a RESTful API that can be consumed by frontend applications or other services.
# The API includes endpoints for greeting users, saving session data, searching sessions by name, and retrieving session statistics.

from fastapi import FastAPI, Depends, Query
from pydantic import BaseModel
from sqlmodel import Session as DBSession, select
from contextlib import asynccontextmanager
from sqlmodel import Session
from app.infrastructure.functions import greet
from app.infrastructure.database import create_db, SessionRecord, engine
from app.domain.services import (
    search_sessions_by_name,
    GreetingService
)

def get_db():
    with DBSession(engine) as session:
        yield session


# Dependency to get the GreetingService instance
# The get_service function is defined as a dependency that can be injected into API endpoints. 
# It returns an instance of the GreetingService, which can be used to perform operations related to greeting sessions. 
# This allows for better separation of concerns and makes it easier to manage dependencies within the API.
def get_service(db: Session = Depends(get_db)):
    return GreetingService(db)

# Lifespan event for startup and shutdown tasks
@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db()  # ensures DB tables exist
    yield

# FastAPI instance
app = FastAPI(lifespan=lifespan)

# Request model for session data
class SessionRequest(BaseModel):
    name: str
    greetings: int
    number: int
    farewell: str

# Stats response model
# The StatsResponse model defines the structure of the response for the /stats endpoint. It includes fields for total_sessions, total_greetings, unique_users, and most_used_number. This model is used to ensure that the response from the /stats endpoint is consistent and well-defined, making it easier for clients to consume the API and understand the data being returned.
class StatsResponse(BaseModel):
    total_sessions: int
    total_greetings: int
    unique_users: int
    most_used_number: int | None
   
# API Endpoints
# The following endpoints are defined for the Greeting App API:
@app.get("/")
def root():
    return {"message": "Greeting App API is running"}


# Endpoint to greet a user
# This endpoint allows clients to greet a user by providing their name and the number of times they want to be greeted. The greet function is called with the provided parameters, and the response includes the greeting message.
@app.get("/greet")
def api_greet(name: str, times: int = Query(1, gt=0)):
    return greet(name, times)


# Endpoint to save session data
# This endpoint allows clients to save session data to the database. It accepts a POST request with a JSON body that matches the SessionRequest model. The save_table_to_file function is called to save the session data to the database, and the response includes a status message and the saved table data.
@app.post("/session")
def api_session(
    data: SessionRequest,
    service: GreetingService = Depends(get_service)
):
    record = service.save_session(
        data.name,
        data.greetings,
        data.number,
        data.farewell
    )
    return {"status": "saved", "id": record.id}

    

# Endpoint to search sessions by name
# This endpoint allows clients to search for sessions by name. It accepts a query parameter for the
@app.get("/sessions/search")
def api_search(name: str, db: Session = Depends(get_db)):
    return search_sessions_by_name(db, name)

# Endpoint to get session statistics
# This endpoint allows clients to retrieve statistics about the greeting sessions. 
# It uses the GreetingService to compute the statistics and returns a response that matches the StatsResponse model, 
# providing information about total sessions, total greetings, unique users, and the most used number.
@app.get("/stats", response_model=StatsResponse)
def api_stats(service: GreetingService = Depends(get_service)):
    return service.get_stats()


