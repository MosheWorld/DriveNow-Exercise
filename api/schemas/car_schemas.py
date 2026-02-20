from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID
from datetime import datetime
from db.car_model import CarStatus

class CarCreate(BaseModel):
    model: str = Field(..., min_length=2)
    year: int = Field(..., ge=1950, json_schema_extra={"example": 2000})
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

class CarUpdate(BaseModel):
    model: Optional[str] = Field(None, min_length=2)
    year: Optional[int] = Field(None, ge=1950, json_schema_extra={"example": 2000})
    status: Optional[CarStatus] = None
