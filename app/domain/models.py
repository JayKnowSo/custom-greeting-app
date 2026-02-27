from typing import Optional
from dataclasses import dataclass


@dataclass
class SessionModel:
    name: str
    greetings: str
    number: int
    farewell: str
    id: Optional[int] = None