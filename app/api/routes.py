# API endpoints for Greeting App using FastAPI
# This file defines the API routes and handlers for the Greeting App, allowing clients to interact with the app's functionality over HTTP.
# It uses FastAPI to create a RESTful API that can be consumed by frontend applications or other services.
# The API includes endpoints for greeting users, saving session data, searching sessions by name, and retrieving session statistics.

from select import select

from fastapi import FastAPI, Query
from app.infrastructure.functions import greet, save_table_to_file, load_sessions, find_sessions_by_name, compute_session_stats, SessionModel
from pydantic import BaseModel
from app.domain.services import save_session_to_db
from app.infrastructure.database import create_db, SessionRecord, engine
from contextlib import asynccontextmanager


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
def api_session(data: SessionRequest):
    table = save_session_to_db(
        data.name,
        data.greetings,
        data.number,
        data.farewell
    )
    return {
        "status": "saved to DB",
        "table": table
    }

# Endpoint to search sessions by name
# This endpoint allows clients to search for session records in the database by providing a name as a query parameter. The load_sessions function is used to retrieve all session records from the database, and the find_sessions_by_name function filters the sessions based on the provided name. The results are returned as a list of matching session records.
@app.get("/sessions/search")
def api_search(name: str):
    with DBSession(engine) as db:
        statement = select(SessionRecord).where(SessionRecord.name.ilike(f"%{name}%"))
        results = db.exec(statement).all()
    return [
        {
            "name": s.name,
            "greetings": s.greetings,
            "number": s.multiplication_number,
            "farewell": s.farewell
        }
        for s in results
    ]

# Endpoint to retrieve session statistics
# This endpoint computes and returns statistics about the sessions stored in the database. It loads all sessions using the load_sessions function, computes the statistics using the compute_session_stats function, and returns the results in a structured format defined by the StatsResponse model.
@app.get("/stats", response_model=StatsResponse)
def api_stats():
    db_sessions = get_all_sessions_from_db()
    stats = {
        "total_sessions": len(db_sessions),
        "total_greetings": sum(s.greetings for s in db_sessions),
        "unique_users": len(set(s.name.lower() for s in db_sessions)),
        "most_used_number": None,
    }

    if db_sessions:
        number_counts = {}
        for s in db_sessions:
            number_counts[s.multiplication_number] = number_counts.get(s.multiplication_number, 0) + 1
        stats["most_used_number"] = max(number_counts, key=number_counts.get)

    return stats
