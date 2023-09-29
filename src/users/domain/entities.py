from dataclasses import dataclass
from datetime import date
from typing import Optional
from uuid import UUID


@dataclass
class Coordinator:
    name: str
    email: str
    password: str
    birth_date: date
    id: Optional[UUID] = None
