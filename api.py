from fastapi import FastAPI
from functions import greet, save_table_to_file, load_sessions, find_sessions_by_name
from pydantic import BaseModel


app = FastAPI()

class SessionRequest(BaseModel):
    name: str
    greetings: int
    number: int
    farewell: str

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

