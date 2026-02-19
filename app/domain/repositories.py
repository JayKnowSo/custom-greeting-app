# repositories.py
# This file defines the repository interfaces for managing session data.
# Repositories provide an abstraction layer for data access, allowing the application to interact with data sources
#  (like databases or files) without needing to know the details of how the data is stored or retrieved.


from abc import ABC, abstractmethod
from typing import List
from app.domain.models import SessionModel

class SessionRepository(ABC):

    
    @abstractmethod
    def add(self, session: SessionModel):
        pass

    @abstractmethod
    def get_by_username(self, username: str) -> List[SessionModel]:
        pass