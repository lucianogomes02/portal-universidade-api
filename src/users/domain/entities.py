from dataclasses import dataclass
from uuid import UUID
from datetime import date


@dataclass
class Coordinator:
    # id: UUID
    name: str
    email: str
    password: str
    birth_date: date
