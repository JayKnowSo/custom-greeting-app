# repositories.py
# This file defines the repository interfaces for managing session data.
# Repositories provide an abstraction layer for data access, allowing the application to interact with data sources
#  (like databases or files) without needing to know the details of how the data is stored or retrieved.

from abc import ABC, abstractmethod
from typing import List
from app.domain.models import SessionModel

class SessionRepository(ABC):

    @abstractmethod
    def add(self, session: SessionModel) -> SessionModel:
        """Save a session and return the saved session (with id)."""
        raise NotImplementedError

    @abstractmethod
    def get_by_username(self, username: str) -> List[SessionModel]:
        """Return all sessions for a username."""
        raise NotImplementedError

    @abstractmethod
    def get_all(self) -> List[SessionModel]:
        """Return all sessions."""
        raise NotImplementedError

    @abstractmethod
    def delete(self, session_id: int) -> bool:
        """Delete a session by ID."""
        raise NotImplementedError