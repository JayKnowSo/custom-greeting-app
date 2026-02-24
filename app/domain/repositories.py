# repositories.py
# This file defines the repository interfaces for managing session data.
# Repositories provide an abstraction layer for data access, allowing the application to interact with data sources
#  (like databases or files) without needing to know the details of how the data is stored or retrieved.


from typing import List
from .models import SessionModel

class SessionRepository:
    def add(self, session: SessionModel) -> SessionModel:
        raise NotImplementedError

    def get_by_username(self, username: str) -> List[SessionModel]:
        raise NotImplementedError

    def get_all(self) -> List[SessionModel]:
        raise NotImplementedError