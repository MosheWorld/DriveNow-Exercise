from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from db.database import get_db
from services.rental_service import RentalService
from api.schemas.rental_schemas import RentalCreate, RentalResponse

router = APIRouter(prefix="/rentals", tags=["rentals"])

@router.get("", response_model=List[RentalResponse])
def get_rentals(db: Session = Depends(get_db)):
    service = RentalService(db)
    return service.get_all_rentals()

@router.post("", response_model=RentalResponse, status_code=status.HTTP_201_CREATED)
def create_rental(rental: RentalCreate, db: Session = Depends(get_db)):
    service = RentalService(db)
    return service.create_rental(car_id=rental.car_id, customer_name=rental.customer_name)

@router.post("/{rental_id}/end", response_model=RentalResponse)
def end_rental(rental_id: UUID, db: Session = Depends(get_db)):
    service = RentalService(db)
    return service.end_rental(rental_id)
