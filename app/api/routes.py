# API endpoints for Greeting App using FastAPI
# This file defines the API routes and handlers for the Greeting App, allowing clients to interact with the app's functionality over HTTP.
# It uses FastAPI to create a RESTful API that can be consumed by frontend applications or other services.
# The API includes endpoints for greeting users, saving session data, searching sessions by name, and retrieving session statistics.


from fastapi import APIRouter, Depends
from sqlmodel import Session, delete

from app.infrastructure.db_repository import SQLSessionRepository
from app.domain.services import GreetingService
from app.domain.models import SessionModel
from app.infrastructure.database import get_db, SessionRecord
from app.api.schemas import SessionCreate, SessionResponse


router = APIRouter()


def get_service(db: Session = Depends(get_db)):
    repo = SQLSessionRepository(db)
    return GreetingService(repo)


@router.get("/clear")
def clear_sessions(db: Session = Depends(get_db)):
    db.exec(delete(SessionRecord))
    db.commit()
    return {"status": "database cleared"}


@router.get("/test")
def test():
    return {"message": "Routes working"}


@router.post("/debug")
def debug_route(data: dict):
    return data


@router.post("/session", response_model=SessionResponse)
def create_session_route(
    data: SessionCreate,
    service: GreetingService = Depends(get_service)
):

    session_model = SessionModel(
        id=None,
        name=data.name,
        greetings=data.greetings,
        number=data.number,
        farewell=data.farewell
    )

    return service.create_session(session_model)


@router.get("/sessions/search", response_model=list[SessionResponse])
def search_sessions(
    name: str,
    service: GreetingService = Depends(get_service)
):
    return service.search_sessions(name)


@router.get("/stats")
def get_stats(service: GreetingService = Depends(get_service)):

    return service.get_stats()
  
