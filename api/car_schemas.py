from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime
from db.models import CarStatus

class CarCreate(BaseModel):
    model: str
    year: int
    status: Optional[CarStatus] = CarStatus.AVAILABLE

class CarResponse(BaseModel):
    id: UUID
    model: str
    year: int
    status: CarStatus
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
