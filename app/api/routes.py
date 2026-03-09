# API endpoints for Greeting App using FastAPI
# This file defines the API routes and handlers for the Greeting App, allowing clients to interact with the app's functionality over HTTP.
# It uses FastAPI to create a RESTful API that can be consumed by frontend applications or other services.
# The API includes endpoints for greeting users, saving session data, searching sessions by name, and retrieving session statistics.


from fastapi import APIRouter, Depends, Request
from sqlmodel import Session, delete
from app.infrastructure.db_repository import UserRepository, SQLSessionRepository
from app.domain.services import GreetingService
from app.domain.models import SessionModel
from app.infrastructure.database import get_db, SessionRecord
from app.api.schemas import SessionCreate, SessionResponse, LoginRequest
from app.security.dependencies import get_current_user, require_admin, require_user, require_readonly
from app.services.auth_service import AuthService
from app.security.limiter import limiter

router = APIRouter()



def get_service(db: Session = Depends(get_db)):
    repo = SQLSessionRepository(db)
    return GreetingService(repo)


@router.get("/clear")
@limiter.limit("10/minute")
def clear_sessions(
    request: Request,
    db: Session = Depends(get_db),
    user=Depends(require_admin)
):
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
@limiter.limit("30/minute")
def create_session_route(
    request: Request,
    data: SessionCreate,
    user=Depends(require_user),
    service: GreetingService = Depends(get_service)
):
    print("User:", user["sub"])
    session_model = SessionModel(**data.model_dump())
    print(f"Creating session: {session_model}")
    return service.create_greeting(session_model)


@router.post("/login", status_code=200)
@limiter.limit("5/minute")
def login(
    request: Request,
    data: LoginRequest,
    db: Session = Depends(get_db)
):
    user_repo = UserRepository(db)
    auth_service = AuthService(user_repo)
    token = auth_service.authenticate_user(data.username, data.password)
    return {"access_token": str(token), "token_type": "bearer"}


@router.get("/sessions/search", response_model=list[SessionResponse])
@limiter.limit("30/minute")
def search_sessions(
    request: Request,
    username: str,
    user=Depends(require_readonly),
    service: GreetingService = Depends(get_service)
):
    return service.search_sessions(username)



  
