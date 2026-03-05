# main.py - Entry point for the Greeting App CLI, sets up FastAPI and includes routes
# This file initializes the FastAPI application, sets up the database, 
# and includes the API routes defined in routes.py. 
# It also contains the main function that runs the CLI interface for the Greeting App.


# Greeting App main.py - Controls flow and menus, calls functions from functions.py
from fastapi import FastAPI
from contextlib import asynccontextmanager
from sqlmodel import SQLModel
from app.infrastructure.functions import engine
from app.api import routes as greetings
from app.error_handling import add_exception_handlers


@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield

app = FastAPI(lifespan=lifespan)

# Add error handlers
add_exception_handlers(app)

app.include_router(greetings.router)

@app.get("/")
def root():
    return {"message": "API is running"}
