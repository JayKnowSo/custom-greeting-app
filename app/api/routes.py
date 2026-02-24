# API endpoints for Greeting App using FastAPI
# This file defines the API routes and handlers for the Greeting App, allowing clients to interact with the app's functionality over HTTP.
# It uses FastAPI to create a RESTful API that can be consumed by frontend applications or other services.
# The API includes endpoints for greeting users, saving session data, searching sessions by name, and retrieving session statistics.

from fastapi import APIRouter, Depends, Body
from sqlmodel import Session, delete
from app.infrastructure.db_repository import SQLSessionRepository
from app.domain.services import GreetingService
from app.domain.models import SessionModel, SessionCreate
from pydantic import BaseModel
from app.infrastructure.database import get_db




# Explicit request schema for the POST body to ensure OpenAPI shows an object
class SessionCreateRequest(BaseModel):
    name: str
    greetings: int
    number: int
    farewell: str
from app.infrastructure.database import get_db
# Use `SessionCreate` from app.domain.models (SQLModel-based) to avoid duplicate definitions

router = APIRouter()

@router.get("/clear")
def clear_sessions(db: Session = Depends(get_db)):
    db.exec(delete(SessionModel))
    db.commit()
    return {"status": "database cleared"}

# Dependency
def get_service(db: Session = Depends(get_db)):
    repo = SQLSessionRepository(db)
    return GreetingService(repo)

# Test endpoint to verify routes are working
@router.get("/test")
def test():
    return {"message": "Routes working"}

@router.post("/debug")
def debug_route(data: dict):
    return data

# Endpoint to create a new greeting session
@router.post("/session", response_model=SessionModel)
def create_session_route(data: SessionCreateRequest, service: GreetingService = Depends(get_service)):
    session = service.create_session(
        name=data.name,
        greetings=data.greetings,
        number=data.number,
        farewell=data.farewell
    )
    return session
    


# Endpoint to search sessions by username
@router.get("/sessions/search", response_model=list[SessionModel])
def search_sessions(
    name: str,
    service: GreetingService = Depends(get_service)
):
    return service.search_sessions(name)

# Endpoint to get session statistics
@router.get("/stats")
def get_stats(
    service: GreetingService = Depends(get_service)
):
    stats = service.get_stats()
    return {
        "total_sessions": stats.get("total_sessions", 0),
        "total_greetings": stats.get("total_greetings", 0),
        "unique_users": stats.get("unique_users", 0),
        "most_used_number": stats.get("most_used_number", 0)
    }
  
