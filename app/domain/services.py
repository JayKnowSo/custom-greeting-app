from app.domain.models import SessionModel
from app.infrastructure.storage import save_session, load_sessions
from typing import List

class GreetingService:

    def create_session(self, data: SessionModel) -> SessionModel:
        greetings = [f"Hello, {data.name}!" for _ in range(data.times)]

        table = [
            f"{data.number} x {i} = {data.number * i}"
            for i in range(1, 11)
   ]

        updated_session = SessionModel(
           name=data.name,
           times=data.times,
           number=data.number,
           greetings=greetings,
           table=table,
           farewell=data.farewell
       )
        save_session(updated_session)

        return updated_session


    def search_sessions(self, username: str) -> List[SessionModel]:
        sessions = load_sessions()
        return [
            s for s in sessions
            if s.name.lower() == username.lower()
        ]