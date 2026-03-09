# main.py - Entry point for the Greeting App CLI, sets up FastAPI and includes routes
# This file initializes the FastAPI application, sets up the database, 
# and includes the API routes defined in routes.py. 
# It also contains the main function that runs the CLI interface for the Greeting App.


from fastapi import FastAPI
from contextlib import asynccontextmanager
from sqlmodel import SQLModel
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from app.infrastructure.functions import engine
from app.api import routes as greetings
from app.error_handling import add_exception_handlers
from app.security.limiter import limiter

@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield

app = FastAPI(lifespan=lifespan)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
add_exception_handlers(app)
app.include_router(greetings.router)

@app.get("/")
def root():
    return {"message": "API is running"}