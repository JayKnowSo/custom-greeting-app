# API endpoints for Greeting App using FastAPI
# This file defines the API routes and handlers for the Greeting App, allowing clients to interact with the app's functionality over HTTP.
# It uses FastAPI to create a RESTful API that can be consumed by frontend applications or other services.
# The API includes endpoints for greeting users, saving session data, searching sessions by name, and retrieving session statistics.

from fastapi import FastAPI
from functions import greet, save_table_to_file, load_sessions, find_sessions_by_name, compute_session_stats
from pydantic import BaseModel
from app.domain.services import GreetingService

# Initialize the greeting service
service = GreetingService()

# FastAPI instance
app = FastAPI()

# Request model for session data
class SessionRequest(BaseModel):
    name: str
    greetings: int
    number: int
    farewell: str

# Stats response model
class StatsResponse(BaseModel):
    total_sessions: int
    total_greetings: int
    unique_users: int
    most_used_number: int | None
   
# API Endpoints
@app.get("/")
def root():
    return {"message": "Greeting App API is running"}

@app.get("/greet")
def api_greet(name: str, times: int):
    return greet(name, times)

@app.post("/session")
def api_session(data: SessionRequest):
    table = save_table_to_file(
        data.name,
        data.greetings,
        data.number,
        data.farewell
    )
    return {
        "status": "saved",
        "table": table
    }

@app.get("/sessions/search")
def api_search(name: str):
    sessions = load_sessions()
    return find_sessions_by_name(sessions, name)

@app.get("/stats", response_model=StatsResponse)
def api_stats():
    sessions = load_sessions()
    return compute_session_stats(sessions)
