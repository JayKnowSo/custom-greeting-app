# API endpoints for Greeting App using FastAPI
# This file defines the API routes and handlers for the Greeting App, allowing clients to interact with the app's functionality over HTTP.
# It uses FastAPI to create a RESTful API that can be consumed by frontend applications or other services.
# The API includes endpoints for greeting users, saving session data, searching sessions by name, and retrieving session statistics.


from fastapi import APIRouter, Depends
from sqlmodel import Session, delete
from app.infrastructure.db_repository import UserRepository, SQLSessionRepository
from app.domain.services import GreetingService
from app.domain.models import SessionModel
from app.infrastructure.database import get_db, SessionRecord
from app.api.schemas import SessionCreate, SessionResponse, LoginRequest
from app.security.dependencies import get_current_user
from app.services.auth_service import AuthService



router = APIRouter()


def get_service(db: Session = Depends(get_db)):
    repo = SQLSessionRepository(db)          # create a repo tied to the DB session
    return GreetingService(repo)       # inject repo into your service
    


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


@router.post("/sessions", response_model=SessionResponse, status_code=201)
def create_session_route(
    data: SessionCreate,
    user=Depends(get_current_user),
    service: GreetingService = Depends(get_service)
):
    print("User:", user["sub"]) # DEBUG: check authenticated user

    session_model = SessionModel(**data.model_dump())
    print(f"Creating session: {session_model}")

    return service.create_greeting(session_model)



@router.post("/login", status_code=200)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user_repo = UserRepository(db)
    auth_service = AuthService(user_repo)

    token = auth_service.authenticate_user(data.username, data.password)

    return {"access_token": str(token), "token_type": "bearer"}


@router.get("/sessions/search", response_model=list[SessionResponse])
def search_sessions(
    username: str,
    service: GreetingService = Depends(get_service)
):
    return service.search_sessions(username)





  
