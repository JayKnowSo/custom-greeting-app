# API endpoints for Greeting App using FastAPI
# This file defines the API routes and handlers for the Greeting App, allowing clients to interact with the app's functionality over HTTP.
# It uses FastAPI to create a RESTful API that can be consumed by frontend applications or other services.
# The API includes endpoints for greeting users, saving session data, searching sessions by name, and retrieving session statistics.

from fastapi import FastAPI, Depends, APIRouter
from contextlib import asynccontextmanager
from app.infrastructure.db_repository import SQLSessionRepository
from app.infrastructure.database import create_db
from app.domain.services import GreetingService
from app.domain.models import SessionModel
from sqlmodel import Session, SQLModel
from app.infrastructure.database import get_db

def get_serice(db: Session = Depends(get_db)):
    repo = SQLSessionRepository(db)
    return GreetingService(repo)

# Lifespan event for startup and shutdown tasks
@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db()  # ensures DB tables exist
    yield

# FastAPI instance
app = FastAPI(lifespan=lifespan)


router = APIRouter()

@router.post("/session")
def api_session(data: SessionRequest, service: GreetingService = Depends(get_serice)):
    record = service.create_session(data)
    return {"status": "saved", "id": record.id}

@router.get("/")
def read_root():
    return {"message": "Hello"}

# Endpoint to save session data
# This endpoint allows clients to save session data to the database. 
# It accepts a POST request with a JSON body that matches the SessionRequest model. 
# The save_table_to_file function is called to save the session data to the database, 
# and the response includes a status message and the saved table data.
@app.post("/session")
def api_session(data: SessionModel):
    record = service.create_session(data)
    return {"status": "saved", "id": record.id}
   
   
# API Endpoints
# The following endpoints are defined for the Greeting App API:
@app.get("/sessions/search")
def api_search(name: str):
    return service.search_sessions(name)


# Endpoint to search sessions by name
# This endpoint allows clients to search for sessions by name. It accepts a query parameter for the
@app.get("/sessions/search")
def api_search(name: str):
    return service.search_sessions(name)

# Endpoint to get session statistics
# This endpoint allows clients to retrieve statistics about the greeting sessions. 
# It returns a JSON object containing the total number of sessions, total greetings, unique users,
#  and the most used multiplication number. 
# The get_stats method of the GreetingService is called to calculate and return these statistics based on the session data stored in the database.
@app.get("/stats")
def api_stats():
    return service.get_stats()


