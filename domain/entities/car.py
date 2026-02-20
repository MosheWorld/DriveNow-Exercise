import enum
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

class CarStatus(enum.Enum):
    AVAILABLE = "available"
    IN_USE = "in_use"
    MAINTENANCE = "under_maintenance"

@dataclass
class CarEntity:
    model: str
    year: int
    id: UUID = field(default_factory=uuid4)
    status: CarStatus = CarStatus.AVAILABLE
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
