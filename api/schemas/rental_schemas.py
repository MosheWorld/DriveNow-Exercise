from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime

class RentalCreate(BaseModel):
    car_id: UUID
    customer_name: str

class RentalResponse(BaseModel):
    id: UUID
    car_id: UUID
    customer_name: str
    start_date: datetime
    end_date: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
